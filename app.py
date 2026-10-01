import os
from flask import Flask
from routes.admin_bp import *
from routes.leitura_bp import leitura_bp
from config import Config
from grafico import grafico
from analise.analisador import *
import random
from datetime import datetime, timedelta
from routes.usuario_bp import user_bp
from config import login_manager
from utils import TipoSensor, INFO_SENSORES, nome_sensor, formatar_numero, formatar_valor, formatar_data, paginar
from analise.associacao_regras import descrever_item
from banco import db
from functools import lru_cache
from plotly.offline import get_plotlyjs

app = Flask(__name__)
app.config.from_object(Config)

app.jinja_env.filters['numero'] = formatar_numero
app.jinja_env.filters['valor'] = formatar_valor
app.jinja_env.filters['data'] = formatar_data
# nomes usados pelos templates
app.jinja_env.filters['valor_medida'] = formatar_valor
app.jinja_env.filters['data_br'] = formatar_data
app.jinja_env.filters['item_regra'] = descrever_item


@app.template_filter("inicial_minuscula")
def inicial_minuscula(texto):
    """'Nitrogênio (N)' -> 'nitrogênio (N)', para usar o nome no meio de uma frase."""
    if len(texto) > 1 and texto[1].isupper():
        return texto
    return texto[:1].lower() + texto[1:]

db.init_app(app)


login_manager.init_app(app)
login_manager.login_view = 'home'

with app.app_context():
    db.create_all()

app.register_blueprint(leitura_bp, url_prefix="/leituras")
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)


# disponível em todos os templates
@app.context_processor
def injetar_dados_projeto():
    return {
        "nome_projeto": app.config["NOME_PROJETO"],
        "sensores_info": INFO_SENSORES,
        "nome_sensor": nome_sensor,
        "paginar": paginar,
        "url_pagina": url_pagina,
        "ano_atual": datetime.now().year,
        "pendentes": contar_pendentes,
    }


def url_pagina(numero):
    """Mesma página e filtros, trocando só o número da página."""
    argumentos = {**request.view_args, **request.args.to_dict(), "pagina": numero}
    return url_for(request.endpoint, **argumentos)


def contar_pendentes():
    """Cadastros esperando aprovação (contador no menu do admin)."""
    from dao.usuarioDAO import UsuarioDAO
    return len(UsuarioDAO.listar_pendentes())


@lru_cache(maxsize=1)
def _plotly_js():
    return get_plotlyjs()


# Plotly servido pelo próprio app (funciona sem internet) e guardado em cache pelo navegador
@app.route("/vendor/plotly.min.js")
def plotly_js():
    resposta = app.response_class(_plotly_js(), mimetype="application/javascript")
    resposta.cache_control.public = True
    resposta.cache_control.max_age = 60 * 60 * 24 * 7
    return resposta




@app.route("/preencher")
def preencher_via_url():

    sensor_id = request.args.get("id")
    tipo = request.args.get("tipo")
    valor = request.args.get("valor")


    if not sensor_id or not tipo or not valor:
        return "Parâmetros obrigatórios: id, tipo, valor", 400

    tipos_validos = [t.value for t in TipoSensor]
    if tipo not in tipos_validos:
        return "Tipo inválido", 400

    try:
        valor = float(valor)
    except:
        return "Valor inválido", 400

    LeituraDAO.salvar(sensor_id, tipo, valor)

    return f"Inserido: {tipo} | {sensor_id} | {valor}", 200




@app.route("/")
def home():
    return render_template('homepage.html')




#rota para gerar um monte de dados


@app.route("/popular")
def popular():

    agora = datetime.now()

    for i in range(200):

        base = agora - timedelta(days=i)

        hora = random.randint(0, 23)
        minuto = random.randint(0, 59)

        data_leitura = base.replace(
            hour=hora,
            minute=minuto,
            second=0,
            microsecond=0
        )

        # valores com alguma relação entre si, como num solo real:
        # solo mais úmido conduz mais e esquenta menos; o sensor estima NPK a partir da condutividade
        umidade = random.uniform(15, 80)
        condutividade = 150 + umidade * 18 + random.uniform(-150, 150)

        valores = {
            TipoSensor.UMIDADE_SOLO: umidade,
            TipoSensor.TEMPERATURA_SOLO: 38 - umidade * 0.2 + random.uniform(-3, 3),
            TipoSensor.CONDUTIVIDADE: condutividade,
            TipoSensor.PH: random.uniform(4.5, 8.5),
            TipoSensor.NITROGENIO: condutividade * 0.05 + random.uniform(-10, 10),
            TipoSensor.FOSFORO: condutividade * 0.02 + random.uniform(-5, 5),
            TipoSensor.POTASSIO: condutividade * 0.09 + random.uniform(-15, 15),
        }

        for tipo_enum, valor in valores.items():

            leitura = Leitura(
                sensor_id="1",
                tipo=tipo_enum.value,
                valor=round(max(valor, 0), 2),
                timestamp=data_leitura
            )

            db.session.add(leitura)

    db.session.commit()

    return "Banco populado com sucesso", 200



@app.errorhandler(404)
def pagina_nao_encontrada(error):
    print("pagina nao encontrada", error)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
