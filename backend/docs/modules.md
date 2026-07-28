# Módulos

Documentação dos módulos existentes no sistema. Cada seção descreve finalidade, classes principais, funções principais e como outros módulos o utilizam.

---

## 1. Core — `app/core/`

### `browser.py` — BrowserManager

**Finalidade**: Motor principal do sistema. Gerencia o ciclo de vida dos navegadores Chrome via Playwright, perfis persistentes, páginas, execução de fluxos e interpretação de passos JSON.

**Arquivo**: `app/core/browser.py`

**Principais classes**:

| Classe | Função |
|---|---|
| `BrowserManager` | Classe central. Gerencia contextos Playwright, locks, perfis, execução de fluxos e passos. |
| `BrowserRunError` | Exceção customizada para erros de execução de fluxo. |
| `SafeDict` | Subclasse de `dict` usada para `str.format_map()` seguro em substituição de variáveis. |

**Principais funções/métodos**:

| Método | Descrição |
|---|---|
| `start()` | Inicia o Playwright. Cria perfil padrão se `PROFILE_DIR` estiver vazio. |
| `stop()` | Fecha todos os contextos e para o Playwright. |
| `create_profile(name)` | Cria diretório e contexto persistente Chrome. |
| `open_profile(name)` | Abre/garante contexto e página para um perfil. |
| `delete_profile(name)` | Remove diretório e fecha contexto. |
| `list_profiles()` | Lista metadados de todos os perfis. |
| `get_page(page_id)` | Retorna uma página Playwright ativa por ID. |
| `is_page_alive(page_id)` | Verifica se uma página ainda existe. |
| `acquire_lock(page_id)` | Adquire lock reentrante para uma página. |
| `release_lock(page_id)` | Libera lock de página. |
| `run_flow(profile, flow_name)` | Executa um fluxo: abre perfil, carrega JSON, itera passos. |
| `_execute_step(page, step, index)` | Interpreta e executa um passo individual (~30 ações suportadas). |
| `_resolve_variables(text)` | Substitui placeholders `{VAR}` por valores do contexto. |
| `_load_flow(name)` | Carrega arquivo JSON de fluxo do disco. |
| `_load_sub_flow(name)` | Carrega sub-fluxo referenciado por um passo `flow`. |

**Ações suportadas em `_execute_step()`**:

| Ação (action) | Alias (português) | Descrição |
|---|---|---|
| `navigate` | `navegar` | Navega para URL |
| `click` | `clicar` | Clique em elemento |
| `fill` | `preencher` | Preenche campo |
| `type` | `digitar` | Digita caractere por caractere |
| `press` | `pressionar` | Pressiona tecla (ex.: Enter) |
| `wait_for_selector` | `aguardar_seletor` | Aguarda elemento aparecer |
| `wait` | `aguardar` | Aguarda N segundos |
| `wait_for_url` | — | Aguarda URL específica |
| `screenshot` | `capturar_tela` | Captura screenshot |
| `scroll` | `rolar` | Scroll na página |
| `extract` | `extrair` | Extrai valor de elemento → variável |
| `select` | `selecionar` | Seleciona opção em `<select>` |
| `hover` | `pairar` | Hover sobre elemento |
| `log` | `registrar` | Registra mensagem no log |
| `loop` | `repetir` | Loop de passos com controle de iteração |
| `set` | — | Define variável manualmente |
| `compare` | `comparar` | Compara variável com valor (if/else) |
| `notify` | — | Envia webhook de notificação |
| `flow` | `fluxo` | Executa sub-fluxo aninhado |
| `monitor` | `monitorar` | Registra e inicia monitor DOM |
| `change_page` | `mudar_pagina` | Troca para outra página aberta |

**Como outros módulos o utilizam**:

- `app/api/routes.py`: Todas as rotas de perfil, fluxo, execução, runtime e páginas chamam `browser_manager`.
- `app/monitor/manager.py`: Recebe referência a `browser_manager` para locks e acesso a páginas.
- `app/monitor/worker.py`: Usa `browser_manager` para locks, obtenção de páginas e frames.

---

### `locks.py` — ReentrantLock

**Finalidade**: Lock reentrante para asyncio. Permite que a mesma `asyncio.Task` adquira o lock múltiplas vezes sem deadlock.

**Arquivo**: `app/core/locks.py`

**Principais classes**:

| Classe | Função |
|---|---|
| `ReentrantLock` | Lock reentrante assíncrono com contador de aquisições por task. |

**Como outros módulos o utilizam**:

- `BrowserManager` cria um `ReentrantLock` por página para evitar acesso concorrente entre execução de fluxo e workers de monitoramento.

---

### `paths.py` — Constantes de Caminhos

**Finalidade**: Define paths absolutos para diretórios principais do projeto.

**Arquivo**: `app/core/paths.py`

**Constantes**:

| Constante | Valor | Uso |
|---|---|---|
| `ROOT` | Raiz do projeto | Base para todos os paths |
| `FLOW_DIR` | `ROOT / "flows"` | Diretório de fluxos JSON |
| `PROFILE_DIR` | `ROOT / "profiles"` | Diretório de perfis Chrome |
| `DATA_DIR` | `ROOT / "data"` | Diretório de dados |

---

### `config.py` e `storage.py`

**Status**: Placeholders. Os arquivos existem (`app/core/config.py`, `app/core/storage.py`) mas não contêm implementação atualmente.

---

## 2. Models — `app/models/`

### `schemas.py` — Schemas da API

**Finalidade**: Modelos Pydantic para validação de requests e responses da API REST.

**Arquivo**: `app/models/schemas.py`

**Principais classes**:

| Classe | Tipo | Descrição |
|---|---|---|
| `ProfileMetadata` | Response | Metadados de um perfil |
| `ProfileCreateRequest` | Request | Body para criar perfil |
| `ProfileOpenRequest` | Request | Body para abrir perfil |
| `ProfileRenameRequest` | Request | Body para renomear |
| `ProfileDefaultRequest` | Request | Body para definir padrão |
| `ProfileOperationResponse` | Response | Resposta genérica de operação de perfil |
| `FlowStep` | Modelo | Schema flexível de passo (extra="allow") |
| `FlowSaveRequest` | Request | Body para salvar fluxo |
| `FlowSavedResponse` | Response | Resposta de fluxo salvo |
| `RunFlowRequest` | Request | Body para executar fluxo |
| `LogEntry` | Modelo | Entrada de log (timestamp, tipo, mensagem) |
| `RunFlowResponse` | Response | Resposta de execução de fluxo |
| `ActionNavigate` | Modelo | Ação de navegação |
| `ActionFill` | Modelo | Ação de preenchimento |
| `ActionClick` | Modelo | Ação de clique |

**Como outros módulos o utilizam**:

- `app/api/routes.py`: Usa como validação de entrada e tipagem de resposta em todos os endpoints.
- `app/core/browser.py`: Referencia `FlowStep` para validação de passos.

---

### `monitor.py` — Modelo Monitor

**Finalidade**: Modelo Pydantic representando um monitor em runtime. Campos privados (`_running_task`) não são serializados.

**Arquivo**: `app/models/monitor.py`

**Campos principais**:

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | `str` (UUID) | Identificador único |
| `name` | `str` | Nome descritivo |
| `status` | `MonitorStatus` | Estado atual (STOPPED/RUNNING/PAUSED/ERROR/NOT_FOUND) |
| `type` | `str` | Tipo (default: "DOM") |
| `profile` | `str` | Nome do perfil associado |
| `page_id` | `str` | ID da página Playwright |
| `frame_id` | `Optional[str]` | ID do frame (se monitorando iframe) |
| `selector` | `str` | Seletor CSS do elemento monitorado |
| `attribute` | `str` | Atributo extraído (default: "textcontent") |
| `interval` | `float` | Intervalo em segundos entre verificações |
| `timeout` | `float` | Timeout para localizar elemento |
| `verification_count` | `int` | Contador de verificações realizadas |
| `changes_count` | `int` | Contador de mudanças detectadas |
| `last_value` | `Optional[str]` | Último valor lido |
| `context` | `dict` | Variáveis de contexto do monitor |
| `on_change` | `list[dict]` | Passos a executar quando há mudança |
| `on_not_found` | `list[dict]` | Passos a executar quando elemento não é encontrado |
| `save_snapshots` | `bool` | Se captura screenshots nas mudanças |
| `max_history` | `int` | Limite de entradas no histórico |

**Como outros módulos o utilizam**:

- `app/api/routes.py`: Retorna monitores nas respostas.
- `app/monitor/manager.py`: Cria, armazena e manipula instâncias.
- `app/monitor/worker.py`: Lê campos de configuração (selector, interval, etc.).
- `app/monitor/storage.py`: Serializa/desserializa via `model_dump()`.

---

## 3. Monitor — `app/monitor/`

### `manager.py` — MonitorManager

**Finalidade**: Singleton gerenciador do ciclo de vida dos monitores. Registra, inicia, pausa, para e remove monitores. Gerencia `asyncio.Task` dos workers.

**Arquivo**: `app/monitor/manager.py`

**Principais funções**:

| Método | Descrição |
|---|---|
| `initialize(base_dir, browser_manager)` | Inicializa com dependências e carrega monitores salvos. |
| `load_monitors()` | Carrega monitores do disco, força status STOPPED. |
| `list_monitors()` | Retorna lista de todos os monitores. |
| `get_monitor(id)` | Obtém um monitor por ID. |
| `register_monitor(**kwargs)` | Cria, salva e retorna novo monitor. |
| `start_monitor(id)` | Inicia worker em background (idempotente). |
| `pause_monitor(id)` | Pausa worker. |
| `stop_monitor(id)` | Para worker. |
| `remove_monitor(id)` | Remove monitor e dados do disco. |
| `trigger_on_change(id, steps)` | Dispara execução de passos `on_change` em nova task. |
| `trigger_on_not_found(id, steps)` | Dispara execução de passos `on_not_found`. |
| `handle_page_closed(page_id)` | Callback: transiciona monitores para ERROR quando página fecha. |

**Singleton**: `monitor_manager = MonitorManager()` — instância global importada diretamente.

**Como outros módulos o utilizam**:

- `app/api/routes.py`: Endpoints de monitor chamam `monitor_manager`.
- `app/core/browser.py`: Passos `monitor` chamam `monitor_manager.register_monitor()` e `start_monitor()`.

---

### `worker.py` — Workers de Monitoramento

**Finalidade**: Loop principal de verificação (`monitor_worker`) e execução de fluxos reativos (`run_on_change`, `run_on_not_found`).

**Arquivo**: `app/monitor/worker.py`

**Principais funções**:

| Função | Descrição |
|---|---|
| `monitor_worker(monitor_id, manager)` | Loop infinito: sleep → lock → localizar elemento → extrair atributo → normalizar → comparar → persistir → disparar on_change/on_not_found. |
| `run_on_change(monitor_id, steps, manager)` | Executa passos quando mudança é detectada. Usa lock da página. |
| `run_on_not_found(monitor_id, steps, manager)` | Executa passos quando elemento não é encontrado. |
| `dom_para_texto(html)` | Converte HTML em descrição textual simples em português (ignora classes/estilos, mantém tags e textos). |

**Fluxo do `monitor_worker`**:
1. Sleep pelo `interval`.
2. Adquire lock da página.
3. Verifica se página ainda existe.
4. Localiza elemento com timeout.
5. Extrai atributo (textContent, innerText, innerHTML, outerHTML ou atributo customizado).
6. Normaliza conteúdo (`normalize_content`).
7. Compara com último valor (`generate_diff`).
8. Se mudou: incrementa contadores, salva diff, opcionalmente captura screenshot, persiste histórico, dispara `on_change`.
9. Se elemento não encontrado: marca NOT_FOUND, persiste entrada, dispara `on_not_found`.
10. Libera lock e salva estado atual.

**Como outros módulos o utilizam**:

- `MonitorManager`: Cria tasks com `monitor_worker`; chama `run_on_change` e `run_on_not_found` em tasks separadas.

---

### `storage.py` — MonitorStorage

**Finalidade**: Persistência em disco dos dados de monitores. Estrutura: `data/monitors/<uuid>/current.json`, `history.jsonl`, `snapshots/`.

**Arquivo**: `app/monitor/storage.py`

**Principais funções**:

| Método | Descrição |
|---|---|
| `save_current(monitor)` | Salva estado atual em `current.json`. |
| `load_all_monitors()` | Carrega todos os `current.json` do disco. |
| `delete_monitor_data(id)` | Remove diretório inteiro do monitor. |
| `append_history(id, entry, max)` | Adiciona entrada ao `history.jsonl` com rotação. |
| `get_history(id)` | Lê e retorna histórico completo. |
| `save_snapshot(id, filename, content)` | Salva screenshot PNG no diretório de snapshots. |
| `get_snapshot_path(id, filename)` | Retorna path para um snapshot específico. |
| `get_snapshots_list(id)` | Lista arquivos de snapshot. |

**Como outros módulos o utilizam**:

- `MonitorManager`: Delega toda persistência ao storage.
- `monitor_worker`: Usa `append_history` e `save_snapshot`.

---

### `diff.py` — Comparação e Diff

**Finalidade**: Normalização de conteúdo extraído e geração de diffs unificados entre valores antigos e novos.

**Arquivo**: `app/monitor/diff.py`

**Principais funções**:

| Função | Descrição |
|---|---|
| `normalize_content(content, attribute)` | Normaliza whitespace, line endings, e (para HTML) limpa comentários e espaços. |
| `generate_diff(old, new)` | Gera diff unificado via `difflib.unified_diff`. |

**Como outros módulos o utilizam**:

- `monitor_worker`: Chama `normalize_content` para comparar valores e `generate_diff` para produzir diff de mudanças.

---

### `types.py` — Enums

**Finalidade**: Define os tipos enumerados usados em todo o subsistema de monitoramento.

**Arquivo**: `app/monitor/types.py`

**Enums**:

| Enum | Valores |
|---|---|
| `MonitorStatus` | `STOPPED`, `RUNNING`, `PAUSED`, `ERROR`, `NOT_FOUND` |
| `MonitorType` | `DOM`, `NETWORK`, `CONSOLE`, `DOWNLOAD`, `REQUEST`, `RESPONSE`, `FILE`, `VARIABLE` |

**Nota**: Apenas `MonitorType.DOM` está efetivamente implementado no worker. Os demais tipos são definidos mas não possuem lógica de extração correspondente.

---

## 4. API — `app/api/`

### `routes.py` — Rotas REST

**Finalidade**: Expor todas as funcionalidades via HTTP REST. Camada fina que delega para os managers.

**Arquivo**: `app/api/routes.py`

**Grupos de endpoints**: Profiles (7), Flows (3), Run (1), Runtime (2), Pages (3), Monitors (9).

Para documentação completa de cada rota, consulte `docs/api.md`.

**Como outros módulos o utilizam**:

- `app/main.py`: Inclui o router com prefixo `/api`.
- Frontend (`static/js/app.js`, `static/pages/monitoring.html`): Consome via `fetch()`.

---

## 5. Frontend — `static/`

### `index.html` — Dashboard Principal

**Finalidade**: SPA que serve como painel de controle central. Gerencia perfis, fluxos e execução de automações.

**Arquivos**: `index.html`, `static/js/app.js`

**Responsabilidades do JS (`app.js`)**:

- Carregar e renderizar lista de perfis (com status de navegador aberto/fechado).
- Carregar e selecionar fluxos.
- Executar fluxos via `POST /api/run`.
- Exibir logs em tempo real no painel.
- Polling de runtime a cada 5 segundos (`GET /api/runtime`).
- CRUD de perfis via modal (criar, renomear, deletar, definir padrão).
- Abrir navegador de perfil.

**Tecnologias**: HTML5, Tailwind CSS (CDN), Lucide Icons (CDN), Vanilla JavaScript (IIFE, sem framework).

### `monitoring.html` — Centro de Monitoramento

**Finalidade**: Dashboard dedicado para visualizar e controlar monitores.

**Arquivo**: `static/pages/monitoring.html`

**Responsabilidades**:

- Polling de monitores a cada 2 segundos (`GET /api/monitors`).
- Exibir métricas (total, running, paused, errors).
- Tabela com lista de monitores e ações (start/pause/stop/delete).
- Side drawer com detalhes do monitor: informações gerais, estado atual, contexto, último diff, snapshots, timeline de histórico.
- Visualizador de screenshots (modal de imagem).
- Controles de ciclo de vida via API (`/start`, `/pause`, `/stop`, delete).

### Outras páginas

- `static/pages/manual.html` — Manual do usuário (estático).
- `static/pages/faq.html` — FAQ (estático).
- `static/pages/blockgenerator/` — Gerador de blocos de fluxo (ferramenta auxiliar).

---

## 6. Flows — `flows/`

**Finalidade**: Diretório de dados contendo arquivos JSON que definem automações. Cada arquivo representa um fluxo reutilizável.

**Arquivos principais**:

| Arquivo | Descrição |
|---|---|
| `principal.json` | Fluxo orquestrador que referencia sub-fluxos via passos `flow`. |
| `LICITACAO.json` | Exemplo simples: aguardar popup e fechar. |
| `LICITANET_LOGIN_CRETA.json` | Login no portal Licitanet (navigate + fill + click). |
| `LICITANET_DISPUTA_CRETA.json` | Automação de disputa. |
| `LICITANET_ESTADO_CRETA.json` | Verificação de estado. |
| `LICITANET_FORNECEDOR.json` | Cadastro/consulta de fornecedor. |
| `LICITANET_MONITOR_006-2026.json` | Fluxo com passos de monitoramento. |
| `FLOW_CRETA/` | Sub-fluxos modulares para Creta. |
| `olds/` | Fluxos depreciados/arquivados. |
| `gerar_drawio.py` | Script utilitário para gerar diagramas a partir dos JSONs. |

**Estrutura de um fluxo**:
```json
{
  "name": "NOME_DO_FLUXO",
  "steps": [
    { "action": "navigate", "url": "https://..." },
    { "action": "fill", "selector": "...", "value": "..." },
    { "action": "click", "selector": "..." }
  ]
}
```

Cada passo aceita campos obrigatórios e opcionais conforme a ação. O schema `FlowStep` usa `extra = "allow"`, permitindo variações nos nomes de campos (ex.: `selector` ou `seletor`, `value` ou `valor`).