from flask import *
from dao.usuarioDAO import *
from dao.leituraDAO import *
from flask_login import login_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from analise.painel import resumo_painel


user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        user = UsuarioDAO.autenticar(email, senha)

        if not user:
            flash("Email ou senha inválidos.", "danger")
            return redirect(url_for("user_bp.login"))

        if not user.aprovado:
            flash("Sua conta ainda está esperando a aprovação do administrador.", "warning")
            return redirect(url_for("user_bp.login"))

        login_user(user)

        return redirect(url_for("user_bp.painel_usuario"))

    return render_template("usuario/login_user.html")

@user_bp.route("/painel")
@login_required
def painel_usuario():
    return render_template("usuario/painel.html", **resumo_painel())



@user_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        if UsuarioDAO.buscar_por_email(email):
            flash("Já existe uma conta com esse email. Entre com ela ou use outro email.", "danger")
            return redirect(url_for("user_bp.cadastro"))

        senha_hash = generate_password_hash(senha)

        UsuarioDAO.cadastrar(nome, email, senha_hash)
        flash("Conta criada. Você poderá entrar assim que o administrador aprovar o cadastro.", "success")
        return redirect(url_for("user_bp.login"))

    return render_template("usuario/cadastro.html")

@user_bp.route("/user", methods=["GET"])
@login_required
def user_list():
    leituras = LeituraDAO.listar_todas()
    # transforma em dicionários simples para o template
    leituras_data = [{
        "id": l.id,
        "sensor_id": l.sensor_id,
        "tipo": l.tipo,
        "valor": getattr(l, "valor", None),
        "timestamp": str(l.timestamp)
    } for l in leituras]
    return render_template("usuario/user_list.html", leituras=leituras_data)


@user_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
