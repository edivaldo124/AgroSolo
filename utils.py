from datetime import datetime
from enum import Enum
from math import ceil

# Medidas do sensor de solo RS485 7 em 1 (Modbus RTU)
class TipoSensor(Enum):
    UMIDADE_SOLO = 'umidade_solo'
    TEMPERATURA_SOLO = 'temperatura_solo'
    CONDUTIVIDADE = 'condutividade'
    PH = 'ph'
    NITROGENIO = 'nitrogenio'
    FOSFORO = 'fosforo'
    POTASSIO = 'potassio'


# Nome, unidade, símbolo e faixa de medição de cada medida.
# min/max são os limites do sensor: valor fora disso é erro de leitura.
# simbolo e cor identificam a medida nas telas e gráficos; casas é quantas casas decimais exibir.
INFO_SENSORES = {
    'umidade_solo': {'nome': 'Umidade do solo', 'unidade': '%', 'icone': '💧', 'simbolo': 'θ', 'cor': '#3B7DD8', 'casas': 1, 'min': 0, 'max': 100},
    'temperatura_solo': {'nome': 'Temperatura do solo', 'unidade': '°C', 'icone': '🌡️', 'simbolo': 'T', 'cor': '#D4573B', 'casas': 1, 'min': -40, 'max': 80},
    'condutividade': {'nome': 'Condutividade elétrica', 'unidade': 'µS/cm', 'icone': '⚡', 'simbolo': 'CE', 'cor': '#8B5CF6', 'casas': 0, 'min': 0, 'max': 20000},
    'ph': {'nome': 'pH', 'unidade': '', 'icone': '🧪', 'simbolo': 'pH', 'cor': '#0E9F8E', 'casas': 2, 'min': 0, 'max': 14},
    'nitrogenio': {'nome': 'Nitrogênio (N)', 'unidade': 'mg/kg', 'icone': '🌱', 'simbolo': 'N', 'cor': '#5A9E2F', 'casas': 0, 'min': 0, 'max': 2000},
    'fosforo': {'nome': 'Fósforo (P)', 'unidade': 'mg/kg', 'icone': '🌿', 'simbolo': 'P', 'cor': '#B7791F', 'casas': 0, 'min': 0, 'max': 2000},
    'potassio': {'nome': 'Potássio (K)', 'unidade': 'mg/kg', 'icone': '🍃', 'simbolo': 'K', 'cor': '#C2417F', 'casas': 0, 'min': 0, 'max': 2000},
}

lista_sensores = [sensor.value for sensor in TipoSensor]


def nome_sensor(tipo):
    info = INFO_SENSORES.get(tipo)
    if not info:
        return tipo
    if info['unidade']:
        return f"{info['nome']} ({info['unidade']})"
    return info['nome']


def formatar_numero(valor, casas=1):
    """Número no padrão brasileiro: 1.234,5 e sinal de menos tipográfico."""
    if valor is None or valor == '':
        return '—'
    try:
        valor = float(valor)
    except (TypeError, ValueError):
        return str(valor)
    texto = f"{valor:,.{casas}f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return texto.replace("-", "−")


def formatar_valor(valor, tipo):
    """Valor de uma medida com as casas decimais e a unidade dela."""
    info = INFO_SENSORES.get(tipo, {})
    texto = formatar_numero(valor, info.get('casas', 2))
    unidade = info.get('unidade')
    return f"{texto} {unidade}" if unidade else texto


def formatar_data(valor, com_hora=True):
    """Data em dd/mm/aaaa (hh:mm). Aceita datetime ou texto ISO."""
    if not valor:
        return '—'
    if isinstance(valor, str):
        try:
            valor = datetime.fromisoformat(valor)
        except ValueError:
            return valor
    return valor.strftime("%d/%m/%Y %H:%M" if com_hora else "%d/%m/%Y")


def paginar(itens, pagina=1, por_pagina=50):
    """Fatia uma lista para exibir em páginas."""
    total = len(itens)
    paginas = max(1, ceil(total / por_pagina))
    pagina = min(max(1, pagina or 1), paginas)
    inicio = (pagina - 1) * por_pagina
    return {
        "itens": itens[inicio:inicio + por_pagina],
        "pagina": pagina,
        "paginas": paginas,
        "total": total,
        "primeiro": inicio + 1 if total else 0,
        "ultimo": min(inicio + por_pagina, total),
    }
