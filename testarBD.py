from analise.analisador import dataframe_medidas, gerar_correlacao_sensor
import app
app = app.app


with app.app_context():
    df = dataframe_medidas()
    print(df.tail(10))

    correlacao, _, aviso = gerar_correlacao_sensor('umidade_solo', 'condutividade')
    print(aviso or correlacao)
