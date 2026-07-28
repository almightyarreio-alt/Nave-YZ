# Fluxo da Aplicação

Fluxo completo desde a entrada do usuário até a execução final, documentado com diagramas Mermaid.

---

## 1. Inicialização do Sistema

```mermaid
sequenceDiagram
    participant Main as main.py
    participant App as app/main.py
    participant BM as BrowserManager
    participant MM as MonitorManager
    participant MS as MonitorStorage

    Main->>App: uvicorn.run("app.main:app")
    App->>App: lifespan.startup
    App->>BM: start()
    BM->>BM: Inicia Playwright
    BM->>BM: Verifica profiles/ (cria default se vazio)
    BM-->>App: pronto
    App->>MM: initialize(base_dir, browser_manager)
    MM->>MS: load_all_monitors()
    MS-->>MM: dados dos monitores salvos
    MM->>MM: força status=STOPPED para todos
    MM-->>App: pronto
    App-->>Main: servidor ouvindo em :8000
```

---

## 2. Dashboard (Frontend)

```mermaid
sequenceDiagram
    participant User as Usuário
    participant FE as index.html + app.js
    participant API as /api/*

    User->>FE: Acessa http://127.0.0.1:8000
    FE->>API: GET /api/profiles
    API-->>FE: lista de perfis
    FE->>API: GET /api/flows
    API-->>FE: lista de fluxos
    FE->>API: GET /api/runtime
    API-->>FE: estado atual (browsers, páginas, última execução)

    loop Polling (5s)
        FE->>API: GET /api/runtime
        API-->>FE: atualiza status
    end
```

---

## 3. Execução de Fluxo (Run Flow)

```mermaid
sequenceDiagram
    participant User as Usuário
    participant FE as Dashboard
    participant API as POST /api/run
    participant BM as BrowserManager
    participant PW as Playwright (Chrome)
    participant MM as MonitorManager

    User->>FE: Seleciona perfil + fluxo, clica "Executar Automação"
    FE->>API: POST /api/run {profile, flow}
    API->>BM: run_flow(profile, flow_name)

    BM->>BM: open_profile() garante contexto Chrome
    BM->>BM: Obtém/cria página
    BM->>BM: acquire_lock(page_id)
    BM->>BM: _load_flow(flow_name) → JSON

    loop Para cada step no JSON
        BM->>BM: _execute_step(page, step, index)

        alt navigate
            BM->>PW: page.goto(url)
        else fill
            BM->>PW: page.fill(selector, value)
        else click
            BM->>PW: page.click(selector)
        else extract
            BM->>PW: page.evaluate(...) → extrai valor
            BM->>BM: armazena em variável
        else compare
            BM->>BM: avalia condição (==, !=, >, <, contains...)
            BM->>BM: executa branch on_true ou on_false
        else flow
            BM->>BM: carrega sub-fluxo e executa recursivamente
        else monitor
            BM->>MM: register_monitor(...)
            MM->>MM: start_monitor(id) → cria asyncio.Task
        else notify
            BM->>PW: requests.post(webhook, payload)
        end

        BM-->>BM: coleta log {timestamp, tipo, mensagem}
    end

    BM->>BM: release_lock(page_id)
    BM-->>API: logs + resultado
    API-->>FE: RunFlowResponse {status, logs, active_browsers, last_execution}
    FE->>FE: Exibe logs no painel
```

---

## 4. Monitoramento Contínuo (Monitor Worker)

```mermaid
flowchart TD
    A[Monitor Registrado] --> B[start_monitor chamado]
    B --> C[asyncio.Task: monitor_worker]
    C --> D[Sleep interval segundos]
    D --> E{Monitor ainda RUNNING?}
    E -- Não --> F[Encerra worker]
    E -- Sim --> G[acquire_lock page_id]
    G --> H{Página ainda viva?}
    H -- Não --> I[status = ERROR, encerra]
    H -- Sim --> J[Localiza elemento por selector]
    J --> K{Elemento encontrado?}
    K -- Não --> L[status = NOT_FOUND]
    L --> M[Persiste entrada NOT_FOUND no histórico]
    M --> N{on_not_found configurado?}
    N -- Sim --> O[Dispara run_on_not_found em task separada]
    N -- Não --> P[release_lock, save_current]
    O --> P
    K -- Sim --> Q[Extrai atributo textContent/innerText/innerHTML/etc]
    Q --> R[Normaliza conteúdo]
    R --> S{Valor mudou?}
    S -- Sim --> T[Incrementa changes_count]
    T --> U[Gera diff]
    U --> V{ save_snapshots? }
    V -- Sim --> W[Captura screenshot PNG]
    V -- Não --> X[Persiste entrada no histórico]
    W --> X
    X --> Y{ on_change configurado? }
    Y -- Sim --> Z[Dispara run_on_change em task separada]
    Y -- Não --> AA[release_lock, save_current]
    Z --> AA
    S -- Não --> AB[Incrementa verification_count]
    AB --> AA
    AA --> D
```

---

## 5. Fluxo Reativo (on_change / on_not_found)

```mermaid
sequenceDiagram
    participant MW as monitor_worker
    participant MM as MonitorManager
    participant Task as asyncio.Task (independente)
    participant BM as BrowserManager
    participant PW as Playwright

    MW->>MM: trigger_on_change(id, steps)
    MM->>Task: asyncio.create_task(run_on_change(id, steps, manager))
    Note over Task: Executa em paralelo, não bloqueia o worker

    Task->>BM: acquire_lock(page_id)
    Task->>BM: get_page(page_id)
    Task->>BM: Define _variables_var.set(monitor.context)
    loop Para cada step em on_change/on_not_found
        Task->>BM: _execute_step(page, step, index)
        BM->>PW: Ação Playwright (click, fill, navigate, notify...)
    end
    Task->>BM: release_lock(page_id)
```

---

## 6. Ciclo de Vida de Páginas

```mermaid
stateDiagram-v2
    [*] --> Criada: open_profile() ou POST /api/pages/{profile}/new
    Criada --> Ativa: página usada em fluxo ou monitor
    Ativa --> Fechada: POST /api/pages/{id}/close
    Fechada --> [*]
    
    note right of Fechada: handle_page_closed() notifica MonitorManager
    note right of Ativa: Monitores associados mantêm referência
    
    state Ativa {
        [*] --> EmUso: fluxo executando
        EmUso --> Livre: fluxo finalizado
        Livre --> Monitorando: worker ativo
        Monitorando --> EmUso: novo fluxo
    }
```

---

## 7. Fluxo Completo — Visão Macro

```mermaid
flowchart LR
    subgraph Entrada
        A[Usuário no Dashboard]
        B[Arquivo JSON em flows/]
    end

    subgraph API
        C[FastAPI routes.py]
    end

    subgraph Core
        D[BrowserManager]
        E[Playwright + Chrome]
    end

    subgraph Monitoramento
        F[MonitorManager]
        G[monitor_worker]
        H[MonitorStorage]
    end

    subgraph Saída
        I[Logs no Dashboard]
        J[Webhook externo]
        K[Dados em data/monitors/]
    end

    A -->|seleciona perfil + fluxo| C
    B -->|carregado por| D
    C -->|delega para| D
    D -->|controla| E
    D -->|passo 'monitor' registra| F
    F -->|inicia task| G
    G -->|persiste em| H
    D -->|retorna logs| C
    C -->|resposta JSON| I
    G -->|ação notify| J
    H -->|arquivos JSON/PNG| K
```

---

## 8. Resolução de Variáveis

```mermaid
flowchart TD
    A[Step contém value: '...{VAR}...'] --> B[_resolve_variables]
    B --> C{Texto contém placeholders?}
    C -- Não --> D[Retorna texto original]
    C -- Sim --> E[SafeDict com _variables]
    E --> F[str.format_map SafeDict]
    F --> G{Placeholder existe em _variables?}
    G -- Sim --> H[Substitui pelo valor]
    G -- Não --> I[Mantém placeholder literal]
    H --> J[Texto resolvido]
    I --> J

    subgraph Fontes de _variables
        K[.env (dotenv)]
        L[Passo 'extract' anterior]
        M[Passo 'set']
        N[Monitor.context]
        O[Loop: _loop_iteration, _loop_total]
    end

    K --> E
    L --> E
    M --> E
    N --> E
    O --> E
```

---

## 9. Shutdown

```mermaid
sequenceDiagram
    participant App as app/main.py
    participant BM as BrowserManager
    participant MM as MonitorManager
    participant Tasks as asyncio.Tasks

    App->>App: lifespan.shutdown
    App->>BM: stop()
    BM->>BM: Fecha todos os contextos Chrome
    BM->>BM: Para Playwright
    BM-->>App: browsers fechados
    Note over Tasks: Tasks pendentes são canceladas pelo loop fechando
    App-->>App: servidor encerrado
```

---

## Resumo de Ações de Fluxo

| Ação | Entrada | Saída | Side Effects |
|---|---|---|---|
| `navigate` | url | log | Muda URL da página |
| `fill` | selector, value | log | Preenche campo |
| `click` | selector | log | Dispara evento click |
| `type` | selector, value | log | Digita caractere por caractere |
| `press` | key | log | Pressiona tecla |
| `wait_for_selector` | selector, timeout | log, var (opcional) | Aguarda elemento |
| `wait` | seconds | log | Aguarda N segundos |
| `wait_for_url` | url | log | Aguarda URL |
| `screenshot` | (none) | log | Salva screenshot |
| `scroll` | pixels | log | Rola página |
| `extract` | selector, attr, var | log, _variables atualizado | Popula variável |
| `select` | selector, value | log | Seleciona opção |
| `hover` | selector | log | Hover |
| `log` | message | log | Registra mensagem |
| `loop` | times, interval, steps | log | Itera sub-passos |
| `set` | var, value | log, _variables atualizado | Define variável |
| `compare` | var, operator, value, on_true, on_false | log, execução condicional | Branching |
| `notify` | webhook, payload | log | POST HTTP externo |
| `flow` | flow (nome JSON) | logs do sub-fluxo | Execução aninhada |
| `monitor` | name, selector, interval, on_change, on_not_found | log | Registra monitor + cria worker |
| `change_page` | page_id | log | Troca página ativa |