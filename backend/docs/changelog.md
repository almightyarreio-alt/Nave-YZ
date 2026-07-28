# Funcionalidades Implementadas

Lista de funcionalidades atualmente existentes no código, agrupadas por módulo. Apenas o que está implementado e funcional.

---

## Core — Gerenciamento de Navegador

**Arquivo**: `app/core/browser.py`

- Inicialização do Playwright com Chromium
- Modo headless=False (sempre com interface gráfica)
- Criação automática de perfil padrão "Perfil Principal"
- Perfis Chrome persistentes com diretório dedicado
- Listagem de perfis com metadados (nome, created_at, last_used, default)
- Criação, abertura, renomeação, exclusão de perfil
- Definição de perfil padrão
- Múltiplos contextos de navegador simultâneos
- Múltiplas páginas por perfil
- Fechamento e criação de páginas
- Troca entre páginas abertas (`change_page`)
- Locks reentrantes por página (`ReentrantLock`)
- Carregamento de variáveis de ambiente (.env) como contexto

---

## Core — Execução de Fluxos

**Arquivo**: `app/core/browser.py`

- Carregamento de fluxos JSON do diretório `flows/`
- Listagem e salvamento de fluxos
- Execução de fluxo (`run_flow`) com lock de página
- Execução de sub-fluxos referenciados (ação `flow`)
- Resolução de placeholders `{VARIAVEL}` via `SafeDict`
- Fallback de campos com nomes em português (ex.: `seletor` → `selector`)

### Ações de Fluxo (21 implementadas)

| Ação | Suporte |
|---|---|
| `navigate` / `navegar` | Navegação para URL |
| `click` / `clicar` | Clique em elemento |
| `fill` / `preencher` | Preenchimento de campo |
| `type` / `digitar` | Digitação caractere por caractere |
| `press` / `pressionar` | Pressionar tecla (Enter, Tab, etc.) |
| `wait_for_selector` / `aguardar_seletor` | Aguardar elemento + extração opcional |
| `wait` / `aguardar` | Aguardar N segundos |
| `wait_for_url` | Aguardar URL específica |
| `screenshot` / `capturar_tela` | Screenshot da página |
| `scroll` / `rolar` | Scroll vertical |
| `extract` / `extrair` | Extrair atributo de elemento → variável |
| `select` / `selecionar` | Selecionar opção em `<select>` |
| `hover` / `pairar` | Hover sobre elemento |
| `log` / `registrar` | Registrar mensagem no log |
| `loop` / `repetir` | Loop de sub-passos com contador |
| `set` | Definir variável manualmente |
| `compare` / `comparar` | Condicional if/else (8 operadores) |
| `notify` | Enviar webhook HTTP |
| `flow` / `fluxo` | Executar sub-fluxo aninhado |
| `monitor` / `monitorar` | Registrar e iniciar monitor DOM |
| `change_page` / `mudar_pagina` | Trocar para outra página aberta |

### Operadores de `compare`

`==`, `!=`, `>`, `<`, `>=`, `<=`, `contains`, `not_contains`, `startswith`, `endswith`

---

## Monitoramento

### MonitorManager

**Arquivo**: `app/monitor/manager.py`

- Singleton global `monitor_manager`
- Registro de novos monitores
- Inicialização com carregamento de monitores salvos
- Controle de ciclo de vida: start, pause, stop, remove
- Gerenciamento de `asyncio.Task` por monitor
- Idempotência em start (não cria tasks duplicadas)
- Callback `handle_page_closed` para páginas fechadas
- Disparo de ações reativas (`trigger_on_change`, `trigger_on_not_found`)

### Monitor Worker

**Arquivo**: `app/monitor/worker.py`

- Loop contínuo de verificação (`monitor_worker`)
- Aquisição de lock da página antes de verificar
- Localização de elemento com timeout configurável
- Extração de atributos: textContent, innerText, innerHTML, outerHTML, atributos customizados
- Normalização de conteúdo para comparação
- Detecção de mudanças com diff unificado
- Captura opcional de screenshots PNG nas mudanças
- Persistência de histórico em JSONL com rotação
- Execução reativa em tasks separadas (`run_on_change`, `run_on_not_found`)
- Conversão HTML → texto descritivo (`dom_para_texto`)
- Tratamento de elemento não encontrado como status NOT_FOUND (não erro)

### MonitorStorage

**Arquivo**: `app/monitor/storage.py`

- Persistência em `data/monitors/<uuid>/`
- Salvamento de estado atual (`current.json`)
- Carregamento de todos os monitores do disco
- Histórico em formato JSONL com limite rotativo
- Armazenamento e listagem de snapshots PNG
- Exclusão completa de dados de monitor

### Monitor Diff

**Arquivo**: `app/monitor/diff.py`

- Normalização de whitespace e line endings
- Limpeza de comentários HTML para comparação de DOM
- Geração de diff unificado (`difflib.unified_diff`)

---

## API REST

**Arquivo**: `app/api/routes.py` (18 endpoints)

### Perfis (7)

- `GET /api/profiles` — listar
- `POST /api/profiles` — criar
- `POST /api/profiles/open` — abrir navegador
- `GET /api/profiles/{name}` — metadados
- `DELETE /api/profiles/{name}` — remover
- `PUT /api/profiles/{name}/rename` — renomear
- `POST /api/profiles/default` — definir padrão

### Fluxos (3)

- `GET /api/flows` — listar
- `POST /api/flows` — salvar
- `GET /api/flows/{name}` — obter conteúdo

### Execução (1)

- `POST /api/run` — executar fluxo

### Runtime (2)

- `GET /api/runtime` — estado atual
- `GET /api/runtime/logs` — logs da última execução

### Páginas (3)

- `GET /api/pages` — listar ativas
- `POST /api/pages/{id}/close` — fechar
- `POST /api/pages/{profile}/new` — nova em branco

### Monitores (9)

- `GET /api/monitors` — listar
- `POST /api/monitors` — registrar
- `GET /api/monitors/{id}` — obter
- `POST /api/monitors/{id}/start` — iniciar
- `POST /api/monitors/{id}/pause` — pausar
- `POST /api/monitors/{id}/stop` — parar
- `DELETE /api/monitors/{id}` — remover
- `GET /api/monitors/{id}/history` — histórico
- `GET /api/monitors/{id}/snapshots` — listar snapshots
- `GET /api/monitors/{id}/snapshots/{file}` — imagem

---

## Frontend

### Dashboard Principal

**Arquivos**: `index.html`, `static/js/app.js`

- Painel de controle central SPA
- Listagem de perfis com status (navegador aberto/fechado)
- Seleção de perfil ativo e definição como padrão
- Criação de perfil via modal
- Abertura de navegador do perfil
- Exclusão de perfil com confirmação
- Listagem e seleção de fluxos
- Execução de automação com botão Run
- Exibição de logs em tempo real no painel
- Indicadores de status (IDLE / EXECUTANDO)
- Métricas em tempo real (perfis, fluxos, browsers ativos)
- Polling de runtime a cada 5 segundos
- Última execução exibida no painel
- Formatação relativa de datas ("há 5 min", "hoje às 10:30")

### Centro de Monitoramento

**Arquivo**: `static/pages/monitoring.html`

- Dashboard dedicado para monitores (HTML+CSS+JS inline)
- Métricas agregadas (total, running, paused, errors)
- Tabela com lista de monitores e estado em tempo real
- Badges coloridos por status (RUNNING, PAUSED, STOPPED, ERROR, NOT_FOUND)
- Ações por monitor: start, pause, stop, delete
- Side drawer com detalhes completos do monitor
- Exibição de informações gerais (tipo, perfil, page_id, intervalo, timeout)
- Exibição de estado atual (último valor, última mensagem de erro)
- Exibição de contexto de variáveis (JSON formatado)
- Exibição de último diff unificado com syntax highlighting
- Galeria de snapshots com visualizador em modal
- Timeline de histórico de verificações
- Polling automático a cada 2 segundos
- Atualização do drawer sem perder a navegação

### Páginas Auxiliares

- `static/pages/manual.html` — Manual do usuário
- `static/pages/faq.html` — FAQ
- `static/pages/blockgenerator/` — Gerador de blocos de fluxo

---

## Modelos de Dados

**Arquivos**: `app/models/schemas.py`, `app/models/monitor.py`

- `ProfileMetadata` — metadados de perfil
- `ProfileCreateRequest`, `ProfileOpenRequest`, `ProfileRenameRequest`, `ProfileDefaultRequest`
- `ProfileOperationResponse` — resposta genérica de operação
- `FlowStep` — schema flexível de passo (extra="allow")
- `FlowSaveRequest`, `FlowSavedResponse`
- `RunFlowRequest`, `RunFlowResponse`
- `LogEntry` — entrada de log (timestamp, tipo, mensagem)
- `ActionNavigate`, `ActionFill`, `ActionClick`
- `Monitor` — modelo completo com 20+ campos e `_running_task` privado

---

## Utilitários

- `ReentrantLock` assíncrono (`app/core/locks.py`)
- Constantes de caminhos (`app/core/paths.py`)
- Script gerador de diagramas Draw.io (`flows/gerar_drawio.py`)
- Configuração PyInstaller (`Navyauto.spec`)

---

## Fluxos de Exemplo

**Diretório**: `flows/`

- `principal.json` — Fluxo orquestrador com sub-fluxos
- `LICITACAO.json` — Fechar popup modal
- `LICITANET_LOGIN_CRETA.json` — Login com credenciais do .env
- `LICITANET_DISPUTA_CRETA.json` — Automação de disputa
- `LICITANET_ESTADO_CRETA.json` — Verificação de estado
- `LICITANET_FORNECEDOR.json` — Cadastro/consulta
- `LICITANET_MONITOR_006-2026.json` — Fluxo com monitoramento
- `FLOW_CRETA/` — Sub-fluxos modulares