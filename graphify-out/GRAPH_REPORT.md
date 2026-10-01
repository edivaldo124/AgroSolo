# Graph Report - agrosolo  (2026-10-01)

## Corpus Check
- 54 files · ~117,705 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 500 nodes · 777 edges · 39 communities (33 shown, 6 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 40 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1b066920`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- grafico.py
- admin_bp.py
- usuario_bp.py
- What You Must Do When Invoked
- Writing apps with Prisma Composer
- Writing apps with Prisma Composer
- Writing apps with Prisma Composer
- Writing apps with Prisma Composer
- app.py
- LeituraDAO
- graphify reference: extra exports and benchmark
- analisador.py
- graphify reference: query, path, explain
- AgroSolo
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- sidebar.js
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- CLAUDE.md
- .claude/CLAUDE.md
- extraction-spec.md
- demo.tsx
- draggable-widget-grid.tsx
- app.js
- card.tsx
- line-charts-1.tsx
- badge-2.tsx
- demo-chart.tsx
- avatar.tsx
- button-1.tsx

## God Nodes (most connected - your core abstractions)
1. `LeituraDAO` - 27 edges
2. `admin_required()` - 21 edges
3. `UsuarioDAO` - 19 edges
4. `Leitura` - 16 edges
5. `Writing apps with Prisma Composer` - 15 edges
6. `Writing apps with Prisma Composer` - 15 edges
7. `Writing apps with Prisma Composer` - 15 edges
8. `Writing apps with Prisma Composer` - 15 edges
9. `contexto_correlacao()` - 13 edges
10. `resumo_painel()` - 12 edges

## Surprising Connections (you probably didn't know these)
- `dataframe_medidas()` --uses--> `LeituraDAO`  [INFERRED]
  analise/analisador.py → dao/leituraDAO.py
- `contexto_correlacao()` --uses--> `LeituraDAO`  [INFERRED]
  analise/analisador.py → dao/leituraDAO.py
- `injetar_dados_projeto()` --indirect_call--> `nome_sensor()`  [INFERRED]
  app.py → utils.py
- `popular()` --calls--> `Leitura`  [INFERRED]
  app.py → modelo/leitura.py
- `LeituraDAO` --uses--> `TipoSensor`  [INFERRED]
  dao/leituraDAO.py → utils.py

## Import Cycles
- None detected.

## Communities (39 total, 6 thin omitted)

### Community 0 - "grafico.py"
Cohesion: 0.16
Nodes (23): contexto_correlacao(), Variáveis da página de correlação (usuário e admin). form é None no GET., aplicar_tema(), _cor(), _eixo_datas(), _faixa_eixo(), gerar_graf(), grafico_correlacao() (+15 more)

### Community 1 - "admin_bp.py"
Cohesion: 0.16
Nodes (28): converter_periodo(), Converte as datas do formulário (AAAA-MM-DD); a data fim inclui o dia inteiro., contar_pendentes(), Cadastros esperando aprovação (contador no menu do admin)., UsuarioDAO, admin_required(), admin_delete(), admin_delete_by_id() (+20 more)

### Community 2 - "usuario_bp.py"
Cohesion: 0.27
Nodes (7): cadastro(), login(), logout(), painel_usuario(), login_required, route, user_list()

### Community 3 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 4 - "Writing apps with Prisma Composer"
Cohesion: 0.10
Nodes (19): Anatomy of a service, Builds are yours, Databases, Deploy config, Deploying, Driving deploys from code, Object Storage, Production pitfalls (+11 more)

### Community 5 - "Writing apps with Prisma Composer"
Cohesion: 0.10
Nodes (19): Anatomy of a service, Builds are yours, Databases, Deploy config, Deploying, Driving deploys from code, Object Storage, Production pitfalls (+11 more)

### Community 6 - "Writing apps with Prisma Composer"
Cohesion: 0.10
Nodes (19): Anatomy of a service, Builds are yours, Databases, Deploy config, Deploying, Driving deploys from code, Object Storage, Production pitfalls (+11 more)

### Community 7 - "Writing apps with Prisma Composer"
Cohesion: 0.10
Nodes (19): Anatomy of a service, Builds are yours, Databases, Deploy config, Deploying, Driving deploys from code, Object Storage, Production pitfalls (+11 more)

### Community 8 - "app.py"
Cohesion: 0.06
Nodes (31): home(), inicial_minuscula(), injetar_dados_projeto(), pagina_nao_encontrada(), _plotly_js(), popular(), preencher_via_url(), route (+23 more)

### Community 9 - "LeituraDAO"
Cohesion: 0.08
Nodes (22): descrever_item(), executar_apriori(), faixa_solo(), gerar_regras_risco(), gerar_regras_solo(), gerar_transacoes(), nivel_medida(), Uma transação por leitura do sensor: o conjunto de rótulos das 7 medidas.… (+14 more)

### Community 10 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 11 - "analisador.py"
Cohesion: 0.32
Nodes (10): dataframe_medidas(), gerar_correlacao_sensor(), Uma linha por leitura do sensor (agrupada por minuto) e uma coluna por medida.…, Correlação de Pearson entre duas medidas, usando as leituras em que as duas…, obter_dataframe_sensores(), regressao_arvore(), regressao_linear_multipla(), regressao_linear_simples() (+2 more)

### Community 12 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 13 - "AgroSolo"
Cohesion: 0.33
Nodes (5): AgroSolo, AgroSolo, Enviando leituras, Onde ajustar, Rodando

### Community 14 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 15 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 16 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 17 - "sidebar.js"
Cohesion: 0.50
Nodes (3): closeBtn, menuBtn, sidebar

### Community 29 - "demo.tsx"
Cohesion: 0.07
Nodes (33): AGENTS, Cost(), DAYS, Demo(), DOT, duration(), EVALS, Failures() (+25 more)

### Community 30 - "draggable-widget-grid.tsx"
Cohesion: 0.10
Nodes (29): Box, Candidate, candidatesFor(), canonical(), choose(), contains(), DEFAULT_ITEMS, DraggableWidgetGrid() (+21 more)

### Community 31 - "app.js"
Cohesion: 0.15
Nodes (15): atualizarBotoesTema(), comTema(), coresTema(), desenhar(), gravar(), iniciarWidgets(), anunciar(), arrastar() (+7 more)

### Community 32 - "card.tsx"
Cohesion: 0.17
Nodes (13): Card(), CardContent(), cardContentVariants, CardContext, CardContextType, CardFooter(), cardFooterVariants, CardHeader() (+5 more)

### Community 34 - "line-charts-1.tsx"
Cohesion: 0.25
Nodes (8): ChartConfig, ChartContext, ChartContextProps, ChartLegendContent(), ChartTooltipContent(), getPayloadConfigFromPayload(), THEMES, useChart()

### Community 35 - "badge-2.tsx"
Cohesion: 0.28
Nodes (7): Badge(), BadgeButton(), BadgeButtonProps, badgeButtonVariants, BadgeDotProps, BadgeProps, badgeVariants

### Community 36 - "demo-chart.tsx"
Cohesion: 0.29
Nodes (3): chartConfig, salesData, TooltipProps

### Community 38 - "button-1.tsx"
Cohesion: 0.50
Nodes (3): Button(), ButtonArrowProps, buttonVariants

## Knowledge Gaps
- **159 isolated node(s):** `salesData`, `chartConfig`, `TooltipProps`, `Kind`, `Widget` (+154 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LeituraDAO` connect `LeituraDAO` to `grafico.py`, `admin_bp.py`, `usuario_bp.py`, `app.py`, `analisador.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `UsuarioDAO` connect `admin_bp.py` to `app.py`, `usuario_bp.py`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Why does `Leitura` connect `LeituraDAO` to `app.py`, `admin_bp.py`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `LeituraDAO` (e.g. with `contexto_correlacao()` and `dataframe_medidas()`) actually correct?**
  _`LeituraDAO` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `UsuarioDAO` (e.g. with `contar_pendentes()` and `Usuario`) actually correct?**
  _`UsuarioDAO` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `salesData`, `chartConfig`, `TooltipProps` to the rest of the system?**
  _159 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `What You Must Do When Invoked` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._