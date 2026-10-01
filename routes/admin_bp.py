from flask import Blueprint, request,  render_template,  redirect, url_for, flash, current_app
from dao.leituraDAO import LeituraDAO
from werkzeug.security import check_password_hash
from modelo.leitura import Leitura
from modelo.admin import Admin
from banco import db
from decorators import admin_required
from dao.usuarioDAO import UsuarioDAO
from flask_login import login_user, logout_user, login_required
from datetime import datetime
from utils import lista_sensores, nome_sensor
from grafico import grafico
from analise.analisador import contexto_correlacao, converter_periodo
from analise.associacao_regras import (
    gerar_regras_solo,
    gerar_regras_risco
)

from analise.regressor import *





admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route("/admin", methods=["GET"])
@login_required
@admin_required
def admin_page():
    leituras = LeituraDAO.listar_todas()
    # transforma em dicionários simples para o template
    leituras_data = [{
        "id": l.id,
        "sensor_id": l.sensor_id,
        "tipo": l.tipo,
        "valor": getattr(l, "valor", None),
        "timestamp": str(l.timestamp)
    } for l in leituras]
    return render_template(
        "admin/admin_panel.html",
        leituras=leituras_data,
        sensores=lista_sensores
    )



@admin_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "GET":
        return render_template("admin/admin_login.html")

    usuario = request.form.get("usuario")
    senha = request.form.get("senha")

    user_hash = current_app.config.get("ADMIN_USER_HASH")
    pass_hash = current_app.config.get("ADMIN_PASSWORD_HASH")

    ok_user = check_password_hash(user_hash, usuario)
    ok_pass = check_password_hash(pass_hash, senha)

    if ok_user and ok_pass:
        login_user(Admin())
        return redirect(url_for("admin_bp.admin_page"))

    flash("Usuário ou senha inválidos.", "danger")
    return redirect(url_for("admin_bp.admin_login"))


# Logout
@admin_bp.route("/admin/logout")
@login_required
@admin_required
def admin_logout():
    logout_user()
    flash("Logout efetuado.", "info")
    return redirect(url_for("home"))

@admin_bp.route("/admin/delete", methods=["POST"])
@login_required
@admin_required
def admin_delete():
    sensor = request.form.get("sensor")
    data_inicio = request.form.get("data_inicio")
    data_fim = request.form.get("data_fim")

    if not sensor or not data_inicio or not data_fim:
        flash("Preencha todos os campos!", "danger")
        return redirect(url_for("admin_bp.admin_page"))

    from datetime import datetime
    try:
        d1 = datetime.strptime(data_inicio, "%Y-%m-%d")
        d2 = datetime.strptime(data_fim, "%Y-%m-%d")
    except:
        flash("Datas inválidas!", "danger")
        return redirect(url_for("admin_bp.admin_page"))

    # Buscar leituras do tipo escolhido no intervalo solicitado
    leituras = (
        Leitura.query
        .filter(Leitura.tipo == sensor)
        .filter(Leitura.timestamp >= d1)
        .filter(Leitura.timestamp <= d2)
        .all()
    )

    if not leituras:
        flash("Nenhuma leitura encontrada nesse intervalo!", "warning")
        return redirect(url_for("admin_bp.admin_page"))

    # Apagar tudo
    for l in leituras:
        db.session.delete(l)

    db.session.commit()

    flash(f"{len(leituras)} leituras do sensor '{sensor}' foram removidas.", "success")
    return redirect(url_for("admin_bp.admin_page"))

@admin_bp.route("/admin/delete/<int:id>", methods=["POST"])
@login_required
@admin_required
def admin_delete_by_id(id):
    leitura = Leitura.query.get(id)

    if not leitura:
        flash("Essa leitura não existe mais.", "danger")
        return redirect(url_for("admin_bp.admin_page"))

    db.session.delete(leitura)
    db.session.commit()

    flash("Leitura excluída.", "success")
    return redirect(url_for("admin_bp.admin_page"))


@admin_bp.route("/admin/delete_by_date", methods=["GET", "POST"])
@login_required
@admin_required
def delete_by_date_page():

    if request.method == "POST":

        sensor = request.form.get("sensor")
        data_inicio = request.form.get("data_inicio")
        data_fim = request.form.get("data_fim")

        try:
            inicio, fim = converter_periodo(data_inicio, data_fim)
        except ValueError:
            flash("Datas inválidas. Use o seletor de data dos campos.", "danger")
            return redirect(url_for("admin_bp.delete_by_date_page"))

        removidas = LeituraDAO.deletar_por_data(sensor, inicio, fim)

        if removidas:
            flash(f"{removidas} leituras de {nome_sensor(sensor)} excluídas.", "success")
        else:
            flash(f"Nenhuma leitura de {nome_sensor(sensor)} nesse período. Nada foi excluído.", "info")

        return redirect(
            url_for("admin_bp.delete_by_date_page")
        )

    return render_template(
        "admin/admin_delete_by_date_page.html"
    )


@admin_bp.route("/admin/usuarios/delete/<int:id>", methods=["POST"])
@login_required
@admin_required
def admin_delete_usuario(id):
    UsuarioDAO.deletar(id)
    flash("Usuário excluído.", "success")
    return redirect(url_for("admin_bp.admin_usuarios"))

@admin_bp.route("/admin/usuarios")
@login_required
@admin_required
def admin_usuarios():
    usuarios = UsuarioDAO.listar_aprovados()  # 🔥 aqui
    return render_template("admin/admin_usuarios.html", usuarios=usuarios)

@admin_bp.route("/admin/usuarios/pendentes")
@login_required
@admin_required
def usuarios_pendentes():
    usuarios = UsuarioDAO.listar_pendentes()
    return render_template("admin/admin_pendentes.html", usuarios=usuarios)

@admin_bp.route("/admin/usuarios/aprovar/<int:id>", methods=["POST"])
@login_required
@admin_required
def aprovar_usuario(id):
    UsuarioDAO.aprovar_usuario(id)
    flash("Cadastro aprovado. O usuário já pode entrar.", "success")
    return redirect(url_for("admin_bp.usuarios_pendentes"))

@admin_bp.route("/admin/usuarios/recusar/<int:id>", methods=["POST"])
@login_required
@admin_required
def recusar_usuario(id):
    UsuarioDAO.deletar(id)
    flash("Cadastro recusado.", "info")
    return redirect(url_for("admin_bp.usuarios_pendentes"))

@admin_bp.route("/filtrar", methods=["GET"])
@login_required
@admin_required
def filtrar_leituras():

    sensor_id = request.args.get("sensor_id")
    tipo = request.args.get("tipo")
    valor_min = request.args.get("valor_min")
    valor_max = request.args.get("valor_max")
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    # Conversão de datas (ISO esperado)
    try:
        data_inicio = datetime.fromisoformat(data_inicio) if data_inicio else None
    except Exception:
        data_inicio = None

    try:
        data_fim = datetime.fromisoformat(data_fim) if data_fim else None
    except Exception:
        data_fim = None

    if data_fim:
        data_fim = data_fim.replace(second=59, microsecond=999999)

    # Conversão numérica segura
    try:
        valor_min = float(valor_min) if valor_min else None
    except Exception:
        valor_min = None

    try:
        valor_max = float(valor_max) if valor_max else None
    except Exception:
        valor_max = None



    try:
        leituras = LeituraDAO.filtrar(
            sensor_id=sensor_id,
            tipo=tipo,
            valor_min=valor_min,
            valor_max=valor_max,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
    except ValueError:
        # fallback seguro se tipo for inválido
        leituras = []

    return render_template(
        "admin/admin_panel.html",
        leituras=leituras,
        sensores=lista_sensores
    )


@admin_bp.route("/grafico-filtrado", methods=["GET"])
@login_required
@admin_required
def grafico_filtrado():

    from datetime import datetime

    sensores = lista_sensores

    tipo = request.args.get("tipo")
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    figura = None
    aviso = None

    if tipo:

        query = Leitura.query.filter(Leitura.tipo == tipo)

        # 🔹 filtro por data direto no banco (correto)
        if data_inicio:
            data_inicio = datetime.fromisoformat(data_inicio)
            query = query.filter(Leitura.timestamp >= data_inicio)

        if data_fim:
            data_fim = datetime.fromisoformat(data_fim)
            query = query.filter(Leitura.timestamp <= data_fim)

        leituras = query.order_by(Leitura.timestamp.asc()).all()

        if not leituras:
            aviso = "Nenhuma leitura nesse período. Amplie as datas ou escolha outra medida."
        else:
            figura = grafico.para_json(grafico.gerar_graf(leituras, tipo))

    return render_template(
        "admin/graficoc.html",
        sensores=sensores,
        figura=figura,
        tipo=tipo,
        aviso=aviso
    )

@admin_bp.route("/correlacaosoloadmin", methods=["GET", "POST"])
@login_required
@admin_required
def pagina_correlacao_solo():

    form = request.form if request.method == "POST" else None

    return render_template(
        "correlacao/admin/correlacao_solo_admin.html",
        **contexto_correlacao(form)
    )

#associacoes de regras

@admin_bp.route("/regras/solo")
@login_required
@admin_required
def regras_solo():

    regras = gerar_regras_solo()

    return render_template(
        "associacao/associacao_solo.html",
        regras=regras
    )


@admin_bp.route("/regras/riscos")
@login_required
@admin_required
def regras_risco():

    regras = gerar_regras_risco()

    return render_template(
        "associacao/associacao_risco.html",
        regras=regras
    )



#regressao

@admin_bp.route("/regressor/linear")
@login_required
@admin_required
def regressor_linear():

    resultado = regressao_linear_simples()

    return render_template(
        "regressor/linear.html",
        resultado=resultado
    )


@admin_bp.route("/regressor/multipla")
@login_required
@admin_required
def regressor_multipla():

    resultado = regressao_linear_multipla()

    return render_template(
        "regressor/multipla.html",
        resultado=resultado
    )


@admin_bp.route("/regressor/arvore")
@login_required
@admin_required
def regressor_arvore():

    resultado = regressao_arvore()

    return render_template(
        "regressor/arvore.html",
        resultado=resultado
    )


@admin_bp.route("/regressor/polinomial")
@login_required
@admin_required
def regressor_polinomial():

    resultado = regressao_polinomial()

    return render_template(
        "regressor/polinomial.html",
        resultado=resultado
    )
