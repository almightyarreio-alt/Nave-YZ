# Arquitetura do Sistema

## Visão Geral

Navyauto é uma aplicação **monolito single-process** que roda um servidor FastAPI com Playwright embutido. Não há workers separados, filas ou bancos de dados externos. Toda a comunicação é síncrona via HTTP REST. Tarefas assíncronas (monitoramento) rodam como `asyncio.Task` dentro do mesmo processo.

## Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────┐
│                    main.py (entry point)                 │
│                    uvicorn.run(app)                      │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              app/main.py (FastAPI lifespan)              │
│                                                         │
│  startup:  BrowserManager.start()  + MonitorManager     │
│  shutdown: BrowserManager.stop()                        │
│                                                         │
│  ┌──────────────────┐    ┌──────────────────────────┐   │
│  │   API Layer      │    │   Core Layer              │   │
│  │  (app/api/)      │◄──►│   (app/core/)             │   │
│  │                  │    │                           │   │
│  │  routes.py       │    │  browser.py (BrowserMgr)  │   │
│  │  18 endpoints    │    │  locks.py (ReentrantLock) │   │
│  │                  │    │  paths.py (constants)     │   │
│  └────────┬─────────┘    └──────────┬───────────────┘   │
│           │                         │                    │
│           │                         ▼                    │
│           │              ┌──────────────────────────┐   │
│           │              │   Monitor Subsystem       │   │
│           │              │  (app/monitor/)           │   │
│           │              │                           │   │
│           │              │  manager.py (singleton)   │   │
│           │              │  worker.py (asyncio tasks)│   │
│           │              │  storage.py (JSON files)  │   │
│           │              │  diff.py (comparison)     │   │
│           │              │  types.py (enums)         │   │
│           │              └──────────────────────────┘   │
│           │                                             │
│           ▼                                             │
│  ┌──────────────────┐                                   │
│  │   Models Layer   │                                   │
│  │  (app/models/)   │                                   │
│  │                  │                                   │
│  │  monitor.py      │                                   │
│  │  schemas.py      │                                   │
│  └──────────────────┘                                   │
└─────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│               Frontend (static/)                         │
│                                                         │
│  index.html         ← Dashboard principal (SPA)         │
│  static/js/app.js   ← Lógica do dashboard               │
│  static/pages/monitoring.html ← Centro de monitoramento │
│  static/pages/manual.html     ← Manual do usuário       │
│  static/pages/faq.html        ← FAQ                     │
│  static/pages/blockgenerator/ ← Gerador de blocos       │
└─────────────────────────────────────────────────────────┘
```

## Organização dos Módulos

| Módulo | Diretório | Responsabilidade |
|---|---|---|
| **API** | `app/api/routes.py` | Endpoints REST. Orquestra chamadas ao `BrowserManager` e `MonitorManager`. |
| **Core** | `app/core/` | Motor do sistema: gerenciamento de navegador, locks, paths. |
| **Models** | `app/models/` | Schemas Pydantic para validação de dados da API e modelo de Monitor. |
| **Monitor** | `app/monitor/` | Subsistema independente de monitoramento contínuo de elementos DOM. |
| **Frontend** | `static/` | Interface SPA vanilla JS consumindo API REST. |
| **Flows** | `flows/` | Arquivos JSON declarativos de automação. |

## Fluxo de Execução

1. `main.py` inicia `uvicorn.run("app.main:app")`.
2. No evento `lifespan.startup`:
   - `BrowserManager.start()` lança o Playwright e carrega perfis Chrome se necessário.
   - `MonitorManager.initialize()` carrega monitores salvos do disco.
3. Requisições HTTP chegam às rotas em `routes.py`.
4. Rotas delegam para `BrowserManager` (perfis, fluxos, páginas) ou `MonitorManager` (CRUD de monitores).
5. `BrowserManager.run_flow()` interpreta passos JSON e os executa via Playwright em uma página Chrome.
6. Passos `monitor` registram um `Monitor` no `MonitorManager`, que inicia um `asyncio.Task` (`monitor_worker`) para verificação periódica.
7. No `lifespan.shutdown`, navegadores são fechados e tasks canceladas.

## Responsabilidades de Cada Diretório

| Diretório | Propósito |
|---|---|
| `app/api/` | Expor funcionalidades via REST. NÃO contém lógica de negócio. |
| `app/core/` | Toda a lógica de negócio: navegador, fluxos, execução de passos. |
| `app/models/` | Definições de tipos e validação (Pydantic). |
| `app/monitor/` | Subsistema autônomo de monitoramento. Comunica-se com `BrowserManager` para locks e páginas. |
| `static/` | Frontend. Comunica-se exclusivamente via `fetch()` com a API. |
| `flows/` | Dados declarativos (não código). Lidos pelo `BrowserManager`. |
| `data/` | Persistência local: cache, logs, dados de monitores. |

## Dependências Entre Módulos

```
app/api/routes.py
  → app/core/browser.py     (browser_manager global)
  → app/monitor/manager.py  (monitor_manager global)
  → app/models/schemas.py   (tipos de request/response)
  → app/models/monitor.py   (modelo Monitor)
  → app/monitor/types.py    (enums)

app/core/browser.py
  → app/core/locks.py       (ReentrantLock)
  → app/core/paths.py       (FLOW_DIR, PROFILE_DIR)
  → app/models/schemas.py   (FlowStep)
  → app/monitor/manager.py  (para passos "monitor" registrarem novos monitores)
  → app/monitor/types.py    (MonitorStatus, MonitorType)

app/monitor/manager.py
  → app/models/monitor.py   (Monitor)
  → app/monitor/storage.py  (MonitorStorage)
  → app/monitor/worker.py   (monitor_worker, run_on_change, run_on_not_found)
  → app/monitor/types.py    (MonitorStatus)

app/monitor/worker.py
  → app/monitor/diff.py     (normalize_content, generate_diff)
  → app/monitor/types.py    (MonitorStatus)
  → app/monitor/storage.py  (para persistir histórico/snapshots)

app/monitor/storage.py
  → (apenas stdlib: json, pathlib, shutil)

app/monitor/diff.py
  → (apenas stdlib: difflib, re)
```

## Padrões Arquiteturais

- **Singleton via variável global de módulo**: `browser_manager` (em `browser.py`) e `monitor_manager` (em `manager.py`) são instanciados no nível do módulo e importados diretamente.
- **Locks reentrantes**: `ReentrantLock` (`app/core/locks.py`) permite que a mesma `asyncio.Task` adquira o lock múltiplas vezes (útil em sub-fluxos e monitoramento).
- **Composição sobre herança**: `BrowserManager` compõe Playwright e `MonitorManager`; `MonitorManager` compõe `MonitorStorage` e workers.
- **Stateless API**: As rotas FastAPI não mantêm estado próprio; delegam tudo aos managers.