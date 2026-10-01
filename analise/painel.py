from analise.associacao_regras import nivel_medida, risco_solo, descrever_item
from dao.leituraDAO import LeituraDAO
from utils import lista_sensores


def _caminho_sparkline(valores, largura=120, altura=36):
    """Linha e área (paths SVG) do mini-gráfico das últimas leituras."""
    if len(valores) < 2:
        return None

    minimo, maximo = min(valores), max(valores)
    amplitude = (maximo - minimo) or 1
    passo = largura / (len(valores) - 1)

    pontos = [
        (i * passo, altura - 3 - (v - minimo) / amplitude * (altura - 6))
        for i, v in enumerate(valores)
    ]
    linha = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pontos)

    return {
        "linha": linha,
        "area": f"{linha} L{largura},{altura} L0,{altura} Z",
        "ultimo": pontos[-1],
    }


def resumo_painel(quantidade=30):
    """Dados do painel: última leitura de cada medida, tendência recente e riscos."""
    medidas = []
    riscos = []
    ultima = None

    for tipo in lista_sensores:
        leituras = LeituraDAO.ultimas_do_tipo(tipo, quantidade)
        valores = [l.valor for l in leituras]
        atual = leituras[-1] if leituras else None

        variacao = None
        if len(valores) >= 2:
            variacao = valores[-1] - valores[-2]

        medidas.append({
            "tipo": tipo,
            "atual": atual,
            "nivel": nivel_medida(tipo, atual.valor) if atual else None,
            "variacao": variacao,
            "sparkline": _caminho_sparkline(valores),
            "quantidade": len(valores),
        })

        if atual:
            if ultima is None or atual.timestamp > ultima.timestamp:
                ultima = atual

            rotulo = risco_solo(tipo, atual.valor)
            if rotulo:
                riscos.append({**descrever_item(rotulo), "valor": atual.valor})

    data_min, data_max = LeituraDAO.intervalo_datas()

    return {
        "medidas": medidas,
        "riscos": riscos,
        "ultima": ultima,
        "total": LeituraDAO.contar(),
        "data_min": data_min,
        "data_max": data_max,
        "quantidade": quantidade,
    }
