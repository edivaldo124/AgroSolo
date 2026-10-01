from datetime import datetime, timedelta

import pandas as pd

from dao.leituraDAO import LeituraDAO
from grafico import grafico
from utils import lista_sensores


def dataframe_medidas(data_inicio=None, data_fim=None):
    """
    Uma linha por leitura do sensor (agrupada por minuto) e uma coluna por medida.
    Como o sensor envia as 7 medidas juntas, cada linha tem as 7 preenchidas.
    """
    leituras = LeituraDAO.filtrar(data_inicio=data_inicio, data_fim=data_fim)

    if not leituras:
        return pd.DataFrame(columns=lista_sensores)

    df = pd.DataFrame([{
        "timestamp": l.getTimestamp(),
        "tipo": l.tipo,
        "valor": l.getValor()
    } for l in leituras])

    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.floor("min")

    df = df.pivot_table(index="timestamp", columns="tipo", values="valor", aggfunc="mean")

    return df.reindex(columns=lista_sensores).sort_index()


def converter_periodo(data_inicio, data_fim):
    """Converte as datas do formulário (AAAA-MM-DD); a data fim inclui o dia inteiro."""
    inicio = datetime.strptime(data_inicio, "%Y-%m-%d") if data_inicio else None
    fim = datetime.strptime(data_fim, "%Y-%m-%d") + timedelta(days=1, microseconds=-1) if data_fim else None
    return inicio, fim


def gerar_correlacao_sensor(tipo1, tipo2, data_inicio=None, data_fim=None):
    """
    Correlação de Pearson entre duas medidas, usando as leituras em que as duas
    foram registradas juntas. Retorna (correlacao, df, aviso); correlacao é None quando há aviso.
    """
    if tipo1 not in lista_sensores or tipo2 not in lista_sensores:
        return None, None, "Selecione as duas medidas."

    if tipo1 == tipo2:
        return None, None, "Escolha duas medidas diferentes."

    df = dataframe_medidas(data_inicio, data_fim)[[tipo1, tipo2]].dropna()

    if len(df) < 2:
        return None, df, "⚠ Não há leituras suficientes nesse período."

    correlacao = df[tipo1].corr(df[tipo2])

    if pd.isna(correlacao):
        return None, df, "⚠ Uma das medidas não variou no período, então não há correlação a calcular."

    return round(float(correlacao), 4), df, None


def contexto_correlacao(form=None):
    """Variáveis da página de correlação (usuário e admin). form é None no GET."""
    data_min, data_max = LeituraDAO.intervalo_datas()

    contexto = {
        "data_min": data_min.strftime("%Y-%m-%d") if data_min else None,
        "data_max": data_max.strftime("%Y-%m-%d") if data_max else None,
    }

    if form is None:
        return contexto

    tipo1 = form.get("sensor1")
    tipo2 = form.get("sensor2")

    contexto.update(
        tipo1=tipo1,
        tipo2=tipo2,
        data_inicio=form.get("data_inicio"),
        data_fim=form.get("data_fim"),
    )

    try:
        inicio, fim = converter_periodo(contexto["data_inicio"], contexto["data_fim"])
    except ValueError:
        contexto["aviso"] = "Datas inválidas."
        return contexto

    correlacao, df, aviso = gerar_correlacao_sensor(tipo1, tipo2, inicio, fim)

    if aviso:
        contexto["aviso"] = aviso
        return contexto

    contexto["correlacao"] = correlacao
    contexto["leituras_usadas"] = len(df)
    contexto["figura_serie"] = grafico.para_json(grafico.grafico_correlacao(df, tipo1, tipo2))
    contexto["figura_dispersao"] = grafico.para_json(grafico.grafico_dispersao(df, tipo1, tipo2))

    return contexto
