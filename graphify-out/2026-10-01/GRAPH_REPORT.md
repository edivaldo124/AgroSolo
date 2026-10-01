# Graph Report - agrosolo  (2026-10-01)

## Corpus Check
- 43 files · ~39,238 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 295 nodes · 467 edges · 29 communities (24 shown, 5 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 26 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- LeituraDAO
- admin_bp.py
- Leitura
- What You Must Do When Invoked
- Writing apps with Prisma Composer
- Writing apps with Prisma Composer
- Writing apps with Prisma Composer
- Writing apps with Prisma Composer
- Admin
- associacao_regras.py
- graphify reference: extra exports and benchmark
- regressor.py
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

## God Nodes (most connected - your core abstractions)
1. `LeituraDAO` - 23 edges
2. `admin_required()` - 21 edges
3. `UsuarioDAO` - 17 edges
4. `Leitura` - 16 edges
5. `Writing apps with Prisma Composer` - 15 edges
6. `Writing apps with Prisma Composer` - 15 edges
7. `Writing apps with Prisma Composer` - 15 edges
8. `Writing apps with Prisma Composer` - 15 edges
9. `What You Must Do When Invoked` - 12 edges
10. `contexto_correlacao()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `popular()` --calls--> `Leitura`  [INFERRED]
  app.py → modelo/leitura.py
- `load_user()` --uses--> `Usuario`  [INFERRED]
  config.py → modelo/usuario.py
- `LeituraDAO` --uses--> `Leitura`  [INFERRED]
  dao/leituraDAO.py → modelo/leitura.py
- `admin_page()` --uses--> `LeituraDAO`  [INFERRED]
  routes/admin_bp.py → dao/leituraDAO.py
- `delete_by_date_page()` --uses--> `LeituraDAO`  [INFERRED]
  routes/admin_bp.py → dao/leituraDAO.py

## Import Cycles
- None detected.

## Communities (29 total, 5 thin omitted)

### Community 0 - "LeituraDAO"
Cohesion: 0.09
Nodes (30): contexto_correlacao(), converter_periodo(), dataframe_medidas(), gerar_correlacao_sensor(), Uma linha por leitura do sensor (agrupada por minuto) e uma coluna por medida.…, Converte as datas do formulário (AAAA-MM-DD); a data fim inclui o dia inteiro., Correlação de Pearson entre duas medidas, usando as leituras em que as duas…, Variáveis da página de correlação (usuário e admin). form é None no GET. (+22 more)

### Community 1 - "admin_bp.py"
Cohesion: 0.20
Nodes (24): UsuarioDAO, admin_required(), admin_delete(), admin_delete_by_id(), admin_delete_usuario(), admin_login(), admin_logout(), admin_page() (+16 more)

### Community 2 - "Leitura"
Cohesion: 0.09
Nodes (10): Leitura, UserMixin, Usuario, cadastro(), login(), logout(), painel_usuario(), login_required (+2 more)

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

### Community 8 - "Admin"
Cohesion: 0.18
Nodes (5): Config, load_user(), Admin, UserMixin, user_loader

### Community 9 - "associacao_regras.py"
Cohesion: 0.42
Nodes (8): executar_apriori(), faixa_solo(), gerar_regras_risco(), gerar_regras_solo(), gerar_transacoes(), Uma transação por leitura do sensor: o conjunto de rótulos das 7 medidas.…, Rótulo de risco para valores críticos, ou None., risco_solo()

### Community 10 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 11 - "regressor.py"
Cohesion: 0.67
Nodes (6): obter_dataframe_sensores(), regressao_arvore(), regressao_linear_multipla(), regressao_linear_simples(), regressao_polinomial(), validar_dataframe()

### Community 12 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 13 - "AgroSolo"
Cohesion: 0.40
Nodes (4): AgroSolo, Enviando leituras, Onde ajustar, Rodando

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

## Knowledge Gaps
- **113 isolated node(s):** `menuBtn`, `sidebar`, `closeBtn`, `tsconfig and import specifiers`, `Anatomy of a service` (+108 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LeituraDAO` connect `LeituraDAO` to `admin_bp.py`, `Leitura`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `UsuarioDAO` connect `admin_bp.py` to `Leitura`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `Leitura` connect `Leitura` to `LeituraDAO`, `admin_bp.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `LeituraDAO` (e.g. with `contexto_correlacao()` and `dataframe_medidas()`) actually correct?**
  _`LeituraDAO` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `UsuarioDAO` (e.g. with `Usuario` and `admin_delete_usuario()`) actually correct?**
  _`UsuarioDAO` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `menuBtn`, `sidebar`, `closeBtn` to the rest of the system?**
  _113 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `LeituraDAO` be split into smaller, more focused modules?**
  _Cohesion score 0.08686868686868687 - nodes in this community are weakly interconnected._