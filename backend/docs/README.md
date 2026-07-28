# Navyauto

**Navegador Automatizado** — Orquestrador RPA local-first com FastAPI, Playwright e Chrome persistente.

## Objetivo do Sistema

Automatizar tarefas repetitivas em navegadores web reais (Chrome), utilizando perfis persistentes que mantêm cookies, sessões e estado entre execuções. O sistema executa fluxos definidos em JSON, suportando ações como navegação, preenchimento de formulários, cliques, extração de dados, comparações condicionais e monitoramento contínuo de elementos DOM.

## Tecnologias Utilizadas

| Tecnologia | Finalidade |
|---|---|
| **Python 3** | Linguagem principal do backend |
| **FastAPI** | Framework web para API REST |
| **Uvicorn** | Servidor ASGI |
| **Playwright** | Automação de navegador Chrome |
| **Pydantic** | Validação de dados e schemas |
| **python-dotenv** | Carregamento de variáveis de ambiente (.env) |
| **BeautifulSoup4** | Parsing de HTML para monitoramento |
| **requests** | Notificações HTTP (webhook) |
| **PyInstaller** | Empacotamento para distribuição (.spec) |
| **Tailwind CSS** (CDN) | Estilização do frontend |
| **Lucide Icons** (CDN) | Ícones do dashboard |
| **HTML5 / JavaScript (Vanilla)** | Frontend SPA sem frameworks |

## Estrutura Geral das Pastas

```
navyauto/
├── main.py                  # Entry point: inicia uvicorn
├── index.html               # Frontend SPA (dashboard principal)
├── requirements.txt         # Dependências Python
├── Navyauto.spec            # Configuração PyInstaller
├── app/
│   ├── main.py              # Aplicação FastAPI + lifespan
│   ├── api/
│   │   └── routes.py        # Rotas REST da API
│   ├── core/
│   │   ├── browser.py       # Gerenciador de navegador (BrowserManager)
│   │   ├── config.py        # (placeholder, sem conteúdo atual)
│   │   ├── locks.py         # Lock reentrante para asyncio
│   │   ├── paths.py         # Constantes de caminhos do projeto
│   │   └── storage.py       # (placeholder, sem conteúdo atual)
│   ├── models/
│   │   ├── monitor.py       # Modelo Pydantic do Monitor
│   │   └── schemas.py       # Schemas Pydantic da API
│   └── monitor/
│       ├── manager.py       # Gerenciador de monitores (MonitorManager)
│       ├── worker.py        # Loop de verificação dos monitores
│       ├── storage.py       # Persistência em disco dos monitores
│       ├── diff.py          # Geração de diffs entre valores monitorados
│       └── types.py         # Enums de status e tipo de monitor
├── static/
│   ├── js/
│   │   └── app.js           # Lógica do frontend principal
│   └── pages/
│       ├── monitoring.html  # Página de centro de monitoramento
│       ├── manual.html      # Página de manual do usuário
│       ├── faq.html         # Página de FAQ
│       └── blockgenerator/  # Gerador de blocos de fluxo
├── flows/                   # Fluxos de automação em JSON
│   ├── principal.json       # Fluxo principal (orquestrador)
│   ├── LICITACAO.json       # Exemplo: fechar popup
│   ├── LICITANET_*.json     # Fluxos específicos Licitanet
│   ├── FLOW_CRETA/          # Sub-fluxos Creta
│   ├── olds/                # Fluxos antigos/depreciados
│   └── gerar_drawio.py      # Script auxiliar para gerar diagramas
├── data/
│   ├── cache/               # Cache local
│   ├── logs/                # Logs de execução
│   └── monitors/            # Dados persistentes dos monitores
├── runtime/                 # (vazio, reservado para artefatos de execução)
└── profiles/                # (criado em runtime) Diretórios de perfil Chrome
```

## Como Executar o Projeto

### Pré-requisitos
- Python 3.10+
- Google Chrome instalado
- Playwright com browsers instalados

### Instalação

```bash
pip install -r requirements.txt
playwright install chromium
```

### Configuração

Crie um arquivo `.env` na raiz com as variáveis necessárias (ex.: credenciais). Consulte `docs/configuration.md`.

### Execução

```bash
python main.py
```

O servidor inicia em `http://127.0.0.1:8000`. O dashboard é acessível na raiz (`/`).

### Empacotamento (distribuição)

```bash
pyinstaller Navyauto.spec
```

## Como Desenvolver

1. O backend usa FastAPI com hot-reload automático via uvicorn.
2. O frontend (`index.html` + `static/js/app.js`) é servido como HTML estático e consome a API REST.
3. Fluxos são arquivos JSON no diretório `flows/`.
4. Perfis Chrome são armazenados em `profiles/` (criado automaticamente).
5. Monitores são persistidos em `data/monitors/<uuid>/`.

Para adicionar novas funcionalidades, consulte `docs/developer-guide.md`.

## Fluxo Geral da Aplicação

1. **Inicialização**: `main.py` → `app/main.py` → lifespan inicia `BrowserManager` (Playwright) e `MonitorManager`.
2. **Dashboard**: Usuário acessa `index.html`, que carrega perfis, fluxos e status via API (`/api/profiles`, `/api/flows`, `/api/runtime`).
3. **Execução**: Usuário seleciona um perfil e um fluxo, clica em "Executar Automação" → `POST /api/run` → `BrowserManager.run_flow()`.
4. **Fluxo**: Passos JSON são interpretados sequencialmente (navigate, fill, click, extract, compare, monitor, etc.) e executados no Chrome via Playwright.
5. **Monitoramento**: Passos do tipo `monitor` criam workers em background que verificam periodicamente elementos DOM e disparam ações `on_change` / `on_not_found`.
6. **Resultado**: Logs são retornados ao frontend e exibidos no painel de logs em tempo real.