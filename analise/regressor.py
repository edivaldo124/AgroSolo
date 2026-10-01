from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score

from analise.analisador import dataframe_medidas


# Medida que os regressores tentam prever e as medidas usadas para isso.
# Troque aqui para estudar outra relação (ex.: ALVO = "condutividade").
ALVO = "umidade_solo"
PREDITOR_SIMPLES = "temperatura_solo"
PREDITORES = [
    "temperatura_solo",
    "condutividade",
    "ph",
    "nitrogenio",
    "fosforo",
    "potassio"
]


def obter_dataframe_sensores():

    return dataframe_medidas().dropna()


def validar_dataframe(df, colunas):

    if df.empty:
        return False

    if len(df) < 2:
        return False

    for coluna in colunas:

        if coluna not in df.columns:
            return False

        if df[coluna].isnull().all():
            return False

    return True


def regressao_linear_simples():

    try:

        df = obter_dataframe_sensores()

        if not validar_dataframe(
            df,
            [
                PREDITOR_SIMPLES,
                ALVO
            ]
        ):
            return {
                "erro": "Dados insuficientes para regressão linear simples."
            }

        X = df[[PREDITOR_SIMPLES]]

        y = df[ALVO]

        modelo = LinearRegression()

        modelo.fit(X, y)

        y_pred = modelo.predict(X)

        return {

            "preditor": PREDITOR_SIMPLES,

            "alvo": ALVO,

            "coeficiente":
                round(float(modelo.coef_[0]), 4),

            "intercepto":
                round(float(modelo.intercept_), 4),

            "r2":
                round(float(r2_score(y, y_pred)), 4)

        }

    except Exception as e:

        return {"erro": str(e)}


def regressao_linear_multipla():

    try:

        df = obter_dataframe_sensores()

        if not validar_dataframe(
            df,
            PREDITORES + [ALVO]
        ):
            return {
                "erro": "Dados insuficientes para regressão múltipla."
            }

        X = df[PREDITORES]

        y = df[ALVO]

        modelo = LinearRegression()

        modelo.fit(X, y)

        y_pred = modelo.predict(X)

        return {

            "alvo": ALVO,

            "coeficientes": {
                tipo: round(float(coef), 4)
                for tipo, coef in zip(PREDITORES, modelo.coef_)
            },

            "intercepto":
                round(float(modelo.intercept_), 4),

            "r2":
                round(float(r2_score(y, y_pred)), 4)

        }

    except Exception as e:

        return {"erro": str(e)}


def regressao_arvore():

    try:

        df = obter_dataframe_sensores()

        if not validar_dataframe(
            df,
            PREDITORES + [ALVO]
        ):
            return {
                "erro": "Dados insuficientes para árvore de decisão."
            }

        X = df[PREDITORES]

        y = df[ALVO]

        modelo = DecisionTreeRegressor(
            max_depth=5,
            random_state=42
        )

        modelo.fit(X, y)

        y_pred = modelo.predict(X)

        return {

            "alvo": ALVO,

            "r2":
                round(float(r2_score(y, y_pred)), 4),

            "profundidade":
                modelo.get_depth(),

            "folhas":
                modelo.get_n_leaves(),

            # quanto cada medida pesou nas decisões da árvore (soma 1)
            "importancias": {
                tipo: round(float(imp), 4)
                for tipo, imp in zip(PREDITORES, modelo.feature_importances_)
            }

        }

    except Exception as e:

        return {"erro": str(e)}


def regressao_polinomial():

    try:

        df = obter_dataframe_sensores()

        if not validar_dataframe(
            df,
            [
                PREDITOR_SIMPLES,
                ALVO
            ]
        ):
            return {
                "erro": "Dados insuficientes para regressão polinomial."
            }

        X = df[
            [
                PREDITOR_SIMPLES
            ]
        ]

        y = df[ALVO]

        poly = PolynomialFeatures(
            degree=2
        )

        X_poly = poly.fit_transform(X)

        modelo = LinearRegression()

        modelo.fit(
            X_poly,
            y
        )

        y_pred = modelo.predict(
            X_poly
        )

        return {

            "preditor": PREDITOR_SIMPLES,

            "alvo": ALVO,

            "coeficientes":
                [
                    round(float(v), 4)
                    for v in modelo.coef_
                ],

            "intercepto":
                round(float(modelo.intercept_), 4),

            "r2":
                round(float(r2_score(y, y_pred)), 4)

        }

    except Exception as e:

        return {"erro": str(e)}
