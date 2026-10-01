from plotly import graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

from utils import INFO_SENSORES, nome_sensor


# As cores de texto, grade e fundo do tooltip são trocadas no navegador (static/js/app.js)
# para acompanhar o tema claro/escuro; estas são só o valor inicial.
FONTE = "Archivo, system-ui, sans-serif"
COR_TEXTO = "#6b655d"
COR_GRADE = "rgba(128, 128, 128, 0.25)"


def calcular_media_semanal(leituras):
    if not leituras:
        return pd.DataFrame(columns=["semana", "tipo", "valor"])

    df_sensores = pd.DataFrame([{
        "tipo": l.tipo,
        "valor": l.getValor(),
        "timestamp": l.getTimestamp()
    } for l in leituras])

    df_sensores["timestamp"] = pd.to_datetime(df_sensores["timestamp"])
    df_sensores["semana"] = df_sensores["timestamp"].dt.to_period("W").apply(lambda p: p.start_time.date())

    return (
        df_sensores
        .groupby(["semana", "tipo"], as_index=False)["valor"]
        .mean()
        .sort_values(["semana", "tipo"])
    )


def _cor(tipo):
    return INFO_SENSORES.get(tipo, {}).get("cor", "#2F5E3F")


def _rgba(cor, alfa):
    r, g, b = (int(cor.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alfa})"


def _hover(tipo):
    info = INFO_SENSORES.get(tipo, {})
    unidade = f" {info['unidade']}" if info.get("unidade") else ""
    return f"%{{y:,.{info.get('casas', 2)}f}}{unidade}"


def _faixa_eixo(valores, folga=0.12):
    minimo, maximo = float(np.nanmin(valores)), float(np.nanmax(valores))
    margem = (maximo - minimo) * folga or abs(maximo) * 0.1 or 1
    return [minimo - margem, maximo + margem]


def aplicar_tema(fig):
    """Visual comum a todos os gráficos: fundo transparente, grade tracejada só na horizontal."""
    fig.update_layout(
        template="none",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONTE, size=12, color=COR_TEXTO),
        separators=",.",
        margin=dict(l=4, r=4, t=8, b=4),
        hovermode="x unified",
        hoverlabel=dict(font=dict(family=FONTE, size=12), namelength=-1),
        showlegend=False,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, showline=False, ticks="", automargin=True)
    fig.update_yaxes(
        gridcolor=COR_GRADE, griddash="dash", zeroline=False, showline=False,
        ticks="", automargin=True, separatethousands=True
    )
    return fig


def _eixo_datas(fig):
    fig.update_xaxes(type="date", tickformat="%d/%m", hoverformat="%d/%m/%Y %H:%M")


def para_json(fig):
    """Figura em JSON para o template; app.js desenha com o Plotly do próprio servidor."""
    return fig.to_json().replace("</", "<\\/")


def _linha_faixas(fig, tipo):
    """Linhas de referência nos limites baixo/alto usados nas regras de associação."""
    from analise.associacao_regras import FAIXAS_SOLO

    if tipo not in FAIXAS_SOLO:
        return

    baixo, alto, _ = FAIXAS_SOLO[tipo]
    for valor, texto in ((baixo, "limite baixo"), (alto, "limite alto")):
        fig.add_hline(
            y=valor, line=dict(color=_cor(tipo), width=1, dash="dot"), opacity=0.6,
            annotation=dict(text=texto, font=dict(size=11, color=_cor(tipo)), bgcolor="#ffffff", borderpad=2),
            annotation_position="top left",
        )


def gerar_graf(leituras, tipo):
    if not leituras:
        return False

    df = pd.DataFrame([{
        "valor": l.getValor(),
        "timestamp": l.getTimestamp()
    } for l in leituras])

    df.sort_values("timestamp", inplace=True)

    cor = _cor(tipo)
    faixa = _faixa_eixo(df["valor"])
    # com muitos pontos os marcadores viram borrão; ficam só na série curta
    marcadores = len(df) <= 60

    fig = go.Figure(go.Scatter(
        x=df["timestamp"],
        y=df["valor"],
        name=nome_sensor(tipo),
        mode="lines+markers" if marcadores else "lines",
        line=dict(color=cor, width=2),
        marker=dict(size=9, color="#ffffff", line=dict(color=cor, width=2)),
        fill="tozeroy",
        fillgradient=dict(
            type="vertical", start=faixa[0], stop=faixa[1],
            colorscale=[[0, _rgba(cor, 0)], [1, _rgba(cor, 0.22)]]
        ),
        hovertemplate=_hover(tipo) + "<extra></extra>",
    ))

    aplicar_tema(fig)
    _eixo_datas(fig)
    fig.update_yaxes(range=faixa)
    _linha_faixas(fig, tipo)

    return fig


def grafico_correlacao(df, tipo1, tipo2):
    # cada medida no seu eixo Y, porque as escalas são muito diferentes (ex.: pH e condutividade)
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    for tipo, secundario in ((tipo1, False), (tipo2, True)):
        cor = _cor(tipo)
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df[tipo], name=nome_sensor(tipo), mode="lines",
                line=dict(color=cor, width=2, dash="dash" if secundario else "solid"),
                hovertemplate=_hover(tipo),
            ),
            secondary_y=secundario
        )
        fig.update_yaxes(
            title_text=nome_sensor(tipo), title_font=dict(color=cor),
            secondary_y=secundario
        )

    aplicar_tema(fig)
    _eixo_datas(fig)
    fig.update_yaxes(showgrid=False, secondary_y=True)

    return fig


def grafico_dispersao(df, tipo1, tipo2):
    """Uma medida contra a outra, com a reta de tendência (mínimos quadrados)."""
    x, y = df[tipo1].astype(float), df[tipo2].astype(float)

    fig = go.Figure(go.Scatter(
        x=x, y=y, mode="markers", name="Leituras",
        marker=dict(size=8, color=_rgba(_cor(tipo2), 0.45), line=dict(color=_cor(tipo2), width=1)),
        hovertemplate=f"{nome_sensor(tipo1)}: %{{x:,.{INFO_SENSORES[tipo1]['casas']}f}}<br>"
                      f"{nome_sensor(tipo2)}: %{{y:,.{INFO_SENSORES[tipo2]['casas']}f}}<extra></extra>",
    ))

    if x.nunique() > 1:
        inclinacao, intercepto = np.polyfit(x, y, 1)
        xs = np.array([x.min(), x.max()])
        fig.add_trace(go.Scatter(
            x=xs, y=inclinacao * xs + intercepto, mode="lines", name="Tendência",
            line=dict(color=_cor(tipo1), width=2, dash="dash"), hoverinfo="skip",
        ))

    aplicar_tema(fig)
    fig.update_layout(hovermode="closest")
    fig.update_xaxes(title_text=nome_sensor(tipo1), showgrid=True, gridcolor=COR_GRADE, griddash="dash")
    fig.update_yaxes(title_text=nome_sensor(tipo2))

    return fig
