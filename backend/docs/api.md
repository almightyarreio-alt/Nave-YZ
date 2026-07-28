# Manual da API

**Base URL**: `http://127.0.0.1:8000`

Todas as rotas estão prefixadas com `/api`. Arquivo de implementação: `app/api/routes.py`.

---

## 1. Perfis (Profiles)

### `GET /api/profiles`

Lista todos os perfis Chrome disponíveis.

**Parâmetros**: Nenhum.

**Resposta**: `list[ProfileMetadata]`

```json
[
  {
    "name": "Perfil Principal",
    "created_at": "2026-01-15T10:30:00",
    "last_used": "2026-07-14T09:00:00",
    "default": true
  }
]
```

**Fluxo interno**: `BrowserManager.list_profiles()` → lê subdiretórios de `profiles/` e retorna metadados.

---

### `POST /api/profiles`

Cria um novo perfil Chrome persistente.

**Corpo da requisição**: `ProfileCreateRequest`

```json
{
  "name": "Novo Perfil"
}
```

**Resposta**: `ProfileOperationResponse`

```json
{
  "status": "success",
  "profile": { "name": "Novo Perfil", ... },
  "logs": [{ "timestamp": "...", "tipo": "success", "mensagem": "..." }]
}
```

**Fluxo interno**: `BrowserManager.create_profile(name)` → cria diretório `profiles/<name>/` e inicia contexto Chrome persistente.

---

### `POST /api/profiles/open`

Abre o navegador de um perfil específico (caso não esteja aberto).

**Corpo da requisição**: `ProfileOpenRequest`

```json
{
  "name": "Perfil Principal"
}
```

**Resposta**: `ProfileOperationResponse` com `active_browsers` e `url` da página ativa.

**Fluxo interno**: `BrowserManager.open_profile(name)` → garante que o contexto do perfil e ao menos uma página estejam ativos.

---

### `GET /api/profiles/{profile_name}`

Obtém metadados de um perfil específico.

**Parâmetros**: `profile_name` (path parameter).

**Resposta**: `ProfileMetadata`

**Fluxo interno**: `BrowserManager.get_profile_metadata(name)`.

---

### `DELETE /api/profiles/{profile_name}`

Remove um perfil e todos os seus dados persistentes.

**Parâmetros**: `profile_name` (path parameter).

**Resposta**: `ProfileOperationResponse`

```json
{
  "status": "success",
  "logs": [...]
}
```

**Fluxo interno**: `BrowserManager.delete_profile(name)` → remove diretório `profiles/<name>/` e fecha o contexto associado.

---

### `PUT /api/profiles/{profile_name}/rename`

Renomeia um perfil.

**Corpo da requisição**: `ProfileRenameRequest`

```json
{
  "new_name": "Novo Nome"
}
```

**Resposta**: `ProfileOperationResponse`

---

### `POST /api/profiles/default`

Define um perfil como padrão.

**Corpo da requisição**: `ProfileDefaultRequest`

```json
{
  "name": "Perfil Principal"
}
```

**Resposta**: `ProfileOperationResponse`

---

## 2. Fluxos (Flows)

### `GET /api/flows`

Lista todos os fluxos de automação disponíveis.

**Parâmetros**: Nenhum.

**Resposta**: `list[str]` — nomes dos arquivos JSON em `flows/`.

```json
["LICITACAO", "LICITANET_DISPUTA_CRETA", "LICITANET_ESTADO_CRETA", "LICITANET_FORNECEDOR", "LICITANET_LOGIN_CRETA", "LICITANET_MONITOR_006-2026", "principal"]
```

**Fluxo interno**: Lista arquivos `.json` em `flows/`, excluindo `.gitkeep` e o script `gerar_drawio.py`.

---

### `POST /api/flows`

Salva um novo fluxo de automação.

**Corpo da requisição**: `FlowSaveRequest`

```json
{
  "name": "meu_fluxo",
  "steps": [
    { "action": "navigate", "url": "https://exemplo.com" },
    { "action": "click", "selector": "#btn" }
  ]
}
```

**Resposta**: `FlowSavedResponse`

```json
{
  "status": "saved",
  "flow": "meu_fluxo",
  "path": "meu_fluxo.json"
}
```

**Fluxo interno**: Salva o JSON em `flows/<name>.json`.

---

### `GET /api/flows/{flow_name}`

Obtém o conteúdo de um fluxo específico.

**Parâmetros**: `flow_name` (path parameter).

**Resposta**: Objeto JSON com `name` e `steps`.

**Fluxo interno**: Lê `flows/<flow_name>.json`.

---

## 3. Execução (Run)

### `POST /api/run`

Executa um fluxo de automação em um perfil.

**Corpo da requisição**: `RunFlowRequest`

```json
{
  "profile": "Perfil Principal",
  "flow": "LICITANET_LOGIN_CRETA"
}
```

**Resposta**: `RunFlowResponse`

```json
{
  "status": "success",
  "profile": "Perfil Principal",
  "flow": "LICITANET_LOGIN_CRETA",
  "logs": [
    { "timestamp": "2026-07-14 11:00:00", "tipo": "success", "mensagem": "Passo 1: navegou para https://..." },
    { "timestamp": "2026-07-14 11:00:02", "tipo": "success", "mensagem": "Passo 2: preencheu campo..." }
  ],
  "active_browsers": 1,
  "last_execution": {
    "profile": "Perfil Principal",
    "flow": "LICITANET_LOGIN_CRETA",
    "started_at": "...",
    "finished_at": "...",
    "logs": [...]
  }
}
```

**Fluxo interno**:
1. Garante que o perfil está aberto (`BrowserManager.open_profile()`).
2. Obtém ou cria uma página para o perfil.
3. Carrega o fluxo JSON do disco.
4. Itera sobre os passos chamando `_execute_step()` para cada ação.
5. Coleta logs e retorna ao final.

---

## 4. Runtime

### `GET /api/runtime`

Obtém o estado atual do runtime: navegadores ativos, páginas abertas, última execução.

**Parâmetros**: Nenhum.

**Resposta**:

```json
{
  "active_browsers": 1,
  "active_profiles": ["Perfil Principal"],
  "pages": [
    {
      "profile": "Perfil Principal",
      "page_id": "abc123",
      "url": "https://licitanet.com.br",
      "title": "Licitanet",
      "frame_ids": ["main"]
    }
  ],
  "last_execution": {
    "profile": "Perfil Principal",
    "flow": "LICITANET_LOGIN_CRETA",
    "started_at": "...",
    "finished_at": "...",
    "logs": [...]
  }
}
```

**Fluxo interno**: Agrega informações de `BrowserManager.active_contexts`, `BrowserManager._last_execution`, e enumera páginas abertas.

---

### `GET /api/runtime/logs`

Obtém os logs da última execução.

**Parâmetros**: Nenhum.

**Resposta**: `list[LogEntry]`

```json
[
  { "timestamp": "...", "tipo": "success", "mensagem": "..." }
]
```

---

## 5. Páginas (Pages)

### `GET /api/pages`

Lista todas as páginas ativas em todos os perfis.

**Resposta**:

```json
{
  "pages": [
    { "profile": "...", "page_id": "...", "url": "...", "title": "..." }
  ]
}
```

---

### `POST /api/pages/{page_id}/close`

Fecha uma página específica. Dispara `MonitorManager.handle_page_closed()` para todos os monitores associados.

**Parâmetros**: `page_id` (path parameter).

**Resposta**:

```json
{
  "status": "closed",
  "page_id": "...",
  "affected_monitors": ["uuid1", "uuid2"]
}
```

---

### `POST /api/pages/{profile_name}/new`

Cria uma nova página em branco para um perfil.

**Parâmetros**: `profile_name` (path parameter).

**Resposta**:

```json
{
  "status": "created",
  "page_id": "...",
  "profile": "..."
}
```

---

## 6. Monitores (Monitors)

Implementado em: `app/api/routes.py` (rotas), `app/monitor/manager.py` (lógica), `app/monitor/worker.py` (execução).

### `GET /api/monitors`

Lista todos os monitores registrados com seu estado atual.

**Resposta**: `list[Monitor]`

```json
[
  {
    "id": "uuid",
    "name": "Monitor Chat",
    "status": "RUNNING",
    "type": "DOM",
    "profile": "Perfil Principal",
    "page_id": "abc123",
    "selector": "#chat-messages",
    "attribute": "textcontent",
    "interval": 10.0,
    "verification_count": 45,
    "changes_count": 3,
    "last_check": "2026-07-14T11:00:00",
    "last_value": "Nova mensagem recebida...",
    ...
  }
]
```

---

### `POST /api/monitors`

Registra um novo monitor (não inicia automaticamente).

**Corpo da requisição** (parcial, campos opcionais omitidos):

```json
{
  "name": "Monitor Chat",
  "profile": "Perfil Principal",
  "page_id": "abc123",
  "selector": "#chat-messages",
  "attribute": "textcontent",
  "interval": 5.0,
  "on_change": [
    { "action": "notify", "webhook": "https://hooks.example.com/..." }
  ]
}
```

**Resposta**: `Monitor` (objeto completo com `id` gerado).

---

### `GET /api/monitors/{monitor_id}`

Obtém um monitor específico com seu estado atual.

**Parâmetros**: `monitor_id` (path parameter).

**Resposta**: `Monitor`

---

### `POST /api/monitors/{monitor_id}/start`

Inicia o worker de um monitor (idempotente).

**Resposta**:

```json
{ "status": "started", "monitor_id": "uuid" }
```

---

### `POST /api/monitors/{monitor_id}/pause`

Pausa o worker de um monitor.

**Resposta**:

```json
{ "status": "paused", "monitor_id": "uuid" }
```

---

### `POST /api/monitors/{monitor_id}/stop`

Para o worker de um monitor.

**Resposta**:

```json
{ "status": "stopped", "monitor_id": "uuid" }
```

---

### `DELETE /api/monitors/{monitor_id}`

Remove um monitor e seus dados do disco. Requer que o monitor não esteja RUNNING.

**Resposta**:

```json
{ "status": "deleted", "monitor_id": "uuid" }
```

---

### `GET /api/monitors/{monitor_id}/history`

Obtém o histórico de verificações de um monitor.

**Resposta**: `list[dict]` — entradas do arquivo `history.jsonl`.

```json
[
  {
    "timestamp": "2026-07-14T10:59:50",
    "status": "RUNNING",
    "value": "...",
    "diff": null,
    "snapshot": null,
    "error": null
  },
  {
    "timestamp": "2026-07-14T11:00:00",
    "status": "RUNNING",
    "value": "... (novo valor)",
    "diff": "+ nova linha\n- linha removida",
    "snapshot": "snapshot_20260714_110000.png",
    "error": null
  }
]
```

---

### `GET /api/monitors/{monitor_id}/snapshots`

Lista snapshots (screenshots) disponíveis para um monitor.

**Resposta**: `list[str]` — nomes de arquivos.

```json
["snapshot_20260714_105900.png", "snapshot_20260714_110000.png"]
```

---

### `GET /api/monitors/{monitor_id}/snapshots/{file_name}`

Retorna a imagem do snapshot (binary `image/png`).

---

## Resumo de Endpoints

| Método | URL | Objetivo |
|---|---|---|
| `GET` | `/api/profiles` | Listar perfis |
| `POST` | `/api/profiles` | Criar perfil |
| `POST` | `/api/profiles/open` | Abrir navegador do perfil |
| `GET` | `/api/profiles/{name}` | Metadados de perfil |
| `DELETE` | `/api/profiles/{name}` | Remover perfil |
| `PUT` | `/api/profiles/{name}/rename` | Renomear perfil |
| `POST` | `/api/profiles/default` | Definir perfil padrão |
| `GET` | `/api/flows` | Listar fluxos |
| `POST` | `/api/flows` | Salvar fluxo |
| `GET` | `/api/flows/{name}` | Obter fluxo |
| `POST` | `/api/run` | Executar fluxo |
| `GET` | `/api/runtime` | Estado do runtime |
| `GET` | `/api/runtime/logs` | Logs da última execução |
| `GET` | `/api/pages` | Listar páginas ativas |
| `POST` | `/api/pages/{id}/close` | Fechar página |
| `POST` | `/api/pages/{profile}/new` | Nova página em branco |
| `GET` | `/api/monitors` | Listar monitores |
| `POST` | `/api/monitors` | Registrar monitor |
| `GET` | `/api/monitors/{id}` | Obter monitor |
| `POST` | `/api/monitors/{id}/start` | Iniciar worker |
| `POST` | `/api/monitors/{id}/pause` | Pausar worker |
| `POST` | `/api/monitors/{id}/stop` | Parar worker |
| `DELETE` | `/api/monitors/{id}` | Remover monitor |
| `GET` | `/api/monitors/{id}/history` | Histórico de verificações |
| `GET` | `/api/monitors/{id}/snapshots` | Listar snapshots |
| `GET` | `/api/monitors/{id}/snapshots/{file}` | Imagem do snapshot |