from flask import Blueprint, request, jsonify, render_template, abort
from flask_login import login_required
from dao.leituraDAO import LeituraDAO
from grafico import grafico
from analise.analisador import contexto_correlacao
from utils import lista_sensores, INFO_SENSORES, nome_sensor



leitura_bp = Blueprint("leitura_bp", __name__)

# Recebe uma leitura completa do sensor RS485 7 em 1.
# Aceita GET com query string ou POST com JSON, com as chaves de lista_sensores:
#   /leituras/receber?sensor_id=1&umidade_solo=35.2&temperatura_solo=24.1&condutividade=820
#       &ph=6.4&nitrogenio=45&fosforo=21&potassio=110
@leitura_bp.route('/receber', methods=['GET', 'POST'])
def receber_dados_sensores():
    dados = request.get_json(silent=True) or request.values

    sensor_id = str(dados.get('sensor_id') or '1')

    medidas = {}
    faltando = []

    for tipo in lista_sensores:
        valor = dados.get(tipo)

        if valor is None or valor == '':
            faltando.append(tipo)
            continue

        try:
            valor = float(valor)
        except (TypeError, ValueError):
            return jsonify({"erro": f"Valor inválido para '{tipo}'"}), 400

        info = INFO_SENSORES[tipo]
        if not info['min'] <= valor <= info['max']:
            return jsonify({
                "erro": f"'{tipo}' fora da faixa do sensor ({info['min']} a {info['max']})"
            }), 400

        medidas[tipo] = valor

    if faltando:
        return jsonify({"erro": "Medidas ausentes", "faltando": faltando}), 400

    LeituraDAO.salvar_medidas(sensor_id, medidas)

    return jsonify({"status": "ok", "sensor_id": sensor_id, "medidas": medidas}), 201





# ===========================
# GRAFICO ÚNICO
# ===========================
@leitura_bp.route("/grafico/<string:tipo>")
@login_required
def view_grafico(tipo):
    if tipo not in INFO_SENSORES:
        abort(404)

    leituras = LeituraDAO.get_dados_sensor(tipo) or []

    if not leituras:
        return render_template(
            "usuario/grafico.html",
            tipo=tipo,
            aviso=f"Ainda não há leituras de {nome_sensor(tipo)}. Elas aparecem aqui assim que o sensor enviar dados.",
            figura=None
        )

    valores = [l.valor for l in leituras]
    ultima = max(leituras, key=lambda l: l.timestamp)

    return render_template(
        "usuario/grafico.html",
        tipo=tipo,
        figura=grafico.para_json(grafico.gerar_graf(leituras, tipo)),
        estatisticas={
            "ultima": ultima,
            "minimo": min(valores),
            "media": sum(valores) / len(valores),
            "maximo": max(valores),
            "quantidade": len(valores),
        }
    )




# ===========================
# CORRELAÇÃO ENTRE MEDIDAS DO SOLO
# ===========================
@leitura_bp.route("/correlacaosolo", methods=["GET", "POST"])
@login_required
def pagina_correlacao_solo():

    form = request.form if request.method == "POST" else None

    return render_template(
        "correlacao/usuario/correlacao_solo.html",
        **contexto_correlacao(form)
    )
