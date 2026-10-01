# AgroSolo

Monitoramento de solo com o sensor **RS485 7 em 1** (Modbus RTU): umidade, temperatura,
condutividade elétrica, pH, nitrogênio, fósforo e potássio. Um microcontrolador (ex.: ESP32 + MAX485)
lê o sensor e envia as medidas para este servidor Flask.

## Rodando

```bash
pip install -r requirements.txt
python app.py            # http://localhost:5000
```

- `/popular` gera 200 leituras de teste.
- Admin padrão: usuário `admin`, senha `1234`. Troque com as variáveis `ADMIN_USER_HASH`
  e `ADMIN_PASSWORD_HASH` no `.env` (gere o hash com `hash.py`).

## Enviando leituras

`GET` ou `POST` em `/leituras/receber`, com as 7 medidas na query string ou num JSON:

```
/leituras/receber?sensor_id=1&umidade_solo=35.2&temperatura_solo=24.1&condutividade=820&ph=6.4&nitrogenio=45&fosforo=21&potassio=110
```

| Chave              | Medida                 | Unidade | Faixa aceita |
|--------------------|------------------------|---------|--------------|
| `umidade_solo`     | Umidade                | %       | 0 a 100      |
| `temperatura_solo` | Temperatura            | °C      | -40 a 80     |
| `condutividade`    | Condutividade elétrica | µS/cm   | 0 a 20000    |
| `ph`               | pH                     |         | 0 a 14       |
| `nitrogenio`       | Nitrogênio (N)         | mg/kg   | 0 a 2000     |
| `fosforo`          | Fósforo (P)            | mg/kg   | 0 a 2000     |
| `potassio`         | Potássio (K)           | mg/kg   | 0 a 2000     |

`sensor_id` é opcional (padrão `1`). Envie os valores já convertidos: o sensor costuma
devolver umidade, temperatura e pH multiplicados por 10 nos registradores Modbus.

Respostas: `201` salvou as 7 medidas com o mesmo horário; `400` quando falta medida,
o valor não é número ou está fora da faixa (o JSON da resposta diz qual).

## Onde ajustar

- `utils.py` → `INFO_SENSORES`: nome, unidade e faixa válida de cada medida.
- `analise/associacao_regras.py` → `FAIXAS_SOLO` e `risco_solo`: limites de baixo/médio/alto
  e de risco usados nas regras de associação. São referências genéricas; ajuste para a cultura.
- `analise/regressor.py` → `ALVO`, `PREDITOR_SIMPLES`, `PREDITORES`: o que os regressores preveem.
- `config.py` → `NOME_PROJETO`: nome exibido nas páginas.
# AgroSolo
