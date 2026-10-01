import pandas as pd

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder

from analise.analisador import dataframe_medidas


# ==================================================
# FAIXAS
# ==================================================

# tipo: (limite_baixo, limite_alto, [rótulo abaixo, rótulo entre, rótulo acima])
# Valores de referência genéricos: ajuste para a cultura e o solo do projeto.
FAIXAS_SOLO = {
    "umidade_solo": (30, 70, ["Umidade_Baixa", "Umidade_Media", "Umidade_Alta"]),
    "temperatura_solo": (20, 30, ["Temp_Baixa", "Temp_Media", "Temp_Alta"]),
    "condutividade": (500, 1500, ["CE_Baixa", "CE_Media", "CE_Alta"]),
    "ph": (5.5, 7.5, ["pH_Acido", "pH_Neutro", "pH_Alcalino"]),
    "nitrogenio": (40, 80, ["N_Baixo", "N_Medio", "N_Alto"]),
    "fosforo": (20, 40, ["P_Baixo", "P_Medio", "P_Alto"]),
    "potassio": (80, 160, ["K_Baixo", "K_Medio", "K_Alto"]),
}


def faixa_solo(tipo, valor):

    baixo, alto, rotulos = FAIXAS_SOLO[tipo]

    if valor < baixo:
        return rotulos[0]

    elif valor < alto:
        return rotulos[1]

    return rotulos[2]


def risco_solo(tipo, valor):
    """Rótulo de risco para valores críticos, ou None."""

    if tipo == "umidade_solo" and valor <= 20:
        return "Risco_Seca"

    if tipo == "temperatura_solo" and valor >= 35:
        return "Risco_Calor"

    if tipo == "ph" and valor < 5.0:
        return "Risco_Acidez"

    if tipo == "ph" and valor > 8.0:
        return "Risco_Alcalinidade"

    if tipo == "condutividade" and valor >= 2000:
        return "Risco_Salinidade"

    return None


# ==================================================
# APRIORI GENÉRICO
# ==================================================

def executar_apriori(
        transacoes,
        suporte=0.05,
        confianca=0.70,
        max_itens=3,
        limite=50
):

    if not transacoes:
        return []

    te = TransactionEncoder()

    te_array = te.fit(
        transacoes
    ).transform(transacoes)

    df = pd.DataFrame(
        te_array,
        columns=te.columns_
    )

    # com 7 medidas por transação, limitar o tamanho mantém as regras legíveis
    freq = apriori(
        df,
        min_support=suporte,
        use_colnames=True,
        max_len=max_itens
    )

    if freq.empty:
        return []

    regras = association_rules(
        freq,
        metric="confidence",
        min_threshold=confianca
    )

    if regras.empty:
        return []

    # 7 medidas geram centenas de regras: mostra só as de maior lift
    regras = regras.sort_values(
        by="lift",
        ascending=False
    ).head(limite)

    resultado = []

    for _, row in regras.iterrows():

        resultado.append({

            "antecedente":
                ", ".join(
                    sorted(list(row["antecedents"]))
                ),

            "consequente":
                ", ".join(
                    sorted(list(row["consequents"]))
                ),

            "support":
                round(float(row["support"]), 4),

            "confidence":
                round(float(row["confidence"]), 4),

            "lift":
                round(float(row["lift"]), 4)

        })

    return resultado


# ==================================================
# TRANSAÇÕES
# ==================================================

def gerar_transacoes(rotular):
    """
    Uma transação por leitura do sensor: o conjunto de rótulos das 7 medidas.
    rotular(tipo, valor) devolve o rótulo de cada medida.
    """

    df = dataframe_medidas()

    transacoes = []

    for _, linha in df.iterrows():

        itens = [
            rotular(tipo, valor)
            for tipo, valor in linha.items()
            if pd.notna(valor)
        ]

        if len(itens) >= 2:
            transacoes.append(itens)

    return transacoes


# ==================================================
# SOLO
# ==================================================

def gerar_regras_solo():

    return executar_apriori(
        gerar_transacoes(faixa_solo)
    )


# ==================================================
# RISCO DO SOLO
# ==================================================

def gerar_regras_risco():

    return executar_apriori(
        gerar_transacoes(
            lambda tipo, valor: risco_solo(tipo, valor) or faixa_solo(tipo, valor)
        )
    )


# ==================================================
# TEXTO DOS RÓTULOS NAS TELAS
# ==================================================

# prefixo do rótulo -> medida
_PREFIXOS = {
    "Umidade": "umidade_solo",
    "Temp": "temperatura_solo",
    "CE": "condutividade",
    "pH": "ph",
    "N": "nitrogenio",
    "P": "fosforo",
    "K": "potassio",
}

_NIVEIS = {
    "Baixa": "baixa", "Media": "média", "Alta": "alta",
    "Baixo": "baixo", "Medio": "médio", "Alto": "alto",
    "Acido": "ácido", "Neutro": "neutro", "Alcalino": "alcalino",
}

_NOMES_PREFIXO = {"Temp": "Temperatura"}

_RISCOS = {
    "Risco_Seca": ("Risco de seca", "umidade_solo"),
    "Risco_Calor": ("Risco de calor", "temperatura_solo"),
    "Risco_Acidez": ("Risco de acidez", "ph"),
    "Risco_Alcalinidade": ("Risco de alcalinidade", "ph"),
    "Risco_Salinidade": ("Risco de salinidade", "condutividade"),
}


def descrever_item(rotulo):
    """'Umidade_Baixa' -> {'texto': 'Umidade baixa', 'tipo': 'umidade_solo', 'risco': False}"""
    rotulo = rotulo.strip()

    if rotulo in _RISCOS:
        texto, tipo = _RISCOS[rotulo]
        return {"texto": texto, "tipo": tipo, "risco": True}

    prefixo, _, nivel = rotulo.partition("_")
    nome = _NOMES_PREFIXO.get(prefixo, prefixo)

    return {
        "texto": f"{nome} {_NIVEIS.get(nivel, nivel.lower())}".strip(),
        "tipo": _PREFIXOS.get(prefixo),
        "risco": False,
    }


def nivel_medida(tipo, valor):
    """Faixa da medida (baixa/média/alta, ou ácido/neutro/alcalino) e o tom para exibir."""
    if tipo not in FAIXAS_SOLO or valor is None:
        return None

    baixo, alto, _ = FAIXAS_SOLO[tipo]
    indice = 0 if valor < baixo else 1 if valor < alto else 2

    if tipo == "ph":
        texto = ("Ácido", "Neutro", "Alcalino")[indice]
        tom = ("aviso", "sucesso", "aviso")[indice]
    else:
        texto = ("Faixa baixa", "Faixa média", "Faixa alta")[indice]
        tom = ("info", "sucesso", "aviso")[indice]

    return {"texto": texto, "tom": tom, "baixo": baixo, "alto": alto}
