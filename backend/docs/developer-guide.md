# Guia do Desenvolvedor

Manual para novos desenvolvedores compreenderem e contribuírem com o projeto rapidamente.

---

## Estrutura do Projeto

```
navyauto/
├── main.py                  # Entry point: uvicorn.run("app.main:app")
├── index.html               # Dashboard SPA principal
├── requirements.txt         # Dependências Python
├── Navyauto.spec            # Configuração PyInstaller
├── .env                     # Variáveis de ambiente (não versionado)
├── app/
│   ├── main.py              # FastAPI app + lifespan (startup/shutdown)
│   ├── api/
│   │   └── routes.py        # TODAS as rotas REST (/api/*)
│   ├── core/
│   │   ├── browser.py       # BrowserManager (~1250 linhas, motor principal)
│   │   ├── locks.py         # ReentrantLock assíncrono
│   │   ├── paths.py         # Constantes de caminhos
│   │   ├── config.py        # Placeholder (vazio)
│   │   └── storage.py       # Placeholder (vazio)
│   ├── models/
│   │   ├── monitor.py       # Modelo Pydantic Monitor
│   │   └── schemas.py       # Schemas de request/response da API
│   └── monitor/
│       ├── manager.py       # MonitorManager (singleton)
│       ├── worker.py        # monitor_worker + run_on_change/run_on_not_found
│       ├── storage.py       # Persistência em disco (JSON)
│       ├── diff.py          # Normalização e diff de conteúdo
│       └── types.py         # Enums MonitorStatus, MonitorType
├── static/
│   ├── js/app.js            # Lógica frontend do dashboard
│   └── pages/               # Páginas auxiliares (monitoring, manual, faq, blockgen)
├── flows/                   # Arquivos JSON de automação
├── data/                    # Persistência (cache, logs, monitors/)
├── runtime/                 # Reservado para artefatos de execução
├── profiles/                # (criado em runtime) Perfis Chrome persistentes
└── docs/                    # Documentação do projeto
```

---

## Como Adicionar uma Nova Rota

### 1. Criar schemas (se necessário)

Em `app/models/schemas.py`, adicione modelos Pydantic para request/response:

```python
class MyNewRequest(BaseModel):
    field: str = Field(..., min_length=1)

class MyNewResponse(BaseModel):
    status: str
    data: dict
```

### 2. Adicionar rota em `app/api/routes.py`

```python
@router.post("/my-new-endpoint")
async def my_new_endpoint(request: MyNewRequest):
    result = await browser_manager.some_method(request.field)
    return MyNewResponse(status="success", data=result)
```

### 3. Implementar lógica no módulo apropriado

Se a rota envolve navegador/fluxo → `app/core/browser.py`.
Se a rota envolve monitoramento → `app/monitor/manager.py`.

### 4. Atualizar frontend (se necessário)

Adicione chamadas `fetch()` em `static/js/app.js` ou na página relevante.

---

## Como Adicionar um Novo Módulo

### 1. Criar diretório em `app/`

```
app/
└── mymodule/
    ├── __init__.py
    ├── core.py        # Lógica principal
    └── types.py       # Enums/tipos (opcional)
```

### 2. Seguir o padrão singleton

Se o módulo precisa de estado global, use uma variável no nível do módulo:

```python
# app/mymodule/core.py
class MyManager:
    def __init__(self):
        self._state = {}
    
    def initialize(self, ...):
        ...

my_manager = MyManager()  # singleton global
```

### 3. Integrar no lifespan

Em `app/main.py`, no `lifespan`:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    my_manager.initialize(...)
    yield
    # shutdown
    my_manager.shutdown()
```

### 4. Adicionar rotas

Em `app/api/routes.py`, importe e use `my_manager`.

---

## Como Adicionar um Novo Serviço

Serviços são funcionalidades dentro de módulos existentes. Para adicionar um novo serviço:

### No `BrowserManager` (`app/core/browser.py`)

Adicione métodos à classe `BrowserManager`:

```python
async def my_new_feature(self, param: str) -> dict:
    # ...
    return {"result": "ok"}
```

### No `MonitorManager` (`app/monitor/manager.py`)

Adicione métodos à classe `MonitorManager`:

```python
async def export_monitors(self) -> list[dict]:
    return [m.model_dump() for m in self.monitors.values()]
```

### Adicionar nova ação de fluxo

Para adicionar uma ação suportada em passos de fluxo:

1. Em `app/core/browser.py`, método `_execute_step()`, adicione um novo `if action in {...}`:

```python
if action in {"my_action", "minha_acao"}:
    param = step.get("param", "default")
    # ... lógica
    return self._log("success", f"Passo {index}: ação executada.")
```

2. A ação fica automaticamente disponível em qualquer fluxo JSON.

---

## Convenções Utilizadas

### Nomenclatura

| Contexto | Convenção | Exemplo |
|---|---|---|
| Arquivos Python | snake_case | `browser_manager.py` |
| Classes | PascalCase | `BrowserManager` |
| Funções/métodos | snake_case | `run_flow()` |
| Variáveis globais | snake_case | `browser_manager` |
| Métodos privados | `_` prefixo | `_execute_step()` |
| Constantes | UPPER_SNAKE_CASE | `FLOW_DIR` |
| Rotas API | kebab-case na URL | `/api/my-endpoint` |
| Arquivos JSON fluxo | UPPER_SNAKE_CASE | `LICITANET_LOGIN.json` |

### Código

- **Idioma do código**: Mistura de inglês (estrutural) e português (mensagens, valores de ação). Nomes de métodos e classes são em inglês. Mensagens de log e valores de ação (`navegar`, `clicar`) são em português.
- **Async/await**: Todo o backend é assíncrono. Use `async def` para funções que fazem I/O.
- **Pydantic**: Use `BaseModel` para validação de dados de entrada/saída da API.
- **Tipagem**: Use type hints do Python (`str`, `dict`, `Optional`, etc.).
- **Singleton**: Managers são instanciados como variáveis de módulo e importados diretamente. NÃO use injeção de dependência.

### Fluxos JSON

- Campos de ação aceitam nomes em inglês e português (ex.: `selector` ou `seletor`, `value` ou `valor`).
- Placeholders no formato `{NOME_VARIAVEL}` são substituídos por variáveis de contexto.
- Sub-fluxos são referenciados com ação `flow` e campo `flow` contendo o nome do arquivo JSON.

---

## Fluxo Recomendado para Manutenção

1. **Identificar o arquivo correto**:
   - Problema em rota → `app/api/routes.py`
   - Problema em navegador/perfil/fluxo → `app/core/browser.py`
   - Problema em monitoramento → `app/monitor/`
   - Problema no dashboard → `static/js/app.js` ou `index.html`
   - Problema no centro de monitoramento → `static/pages/monitoring.html`

2. **Reproduzir localmente**:
   ```bash
   python main.py
   ```
   Acessar `http://127.0.0.1:8000`.

3. **Testar via API** (exemplo com curl):
   ```bash
   curl http://127.0.0.1:8000/api/runtime
   curl -X POST http://127.0.0.1:8000/api/run -H "Content-Type: application/json" -d "{\"profile\":\"Perfil Principal\",\"flow\":\"LICITACAO\"}"
   ```

4. **Verificar logs**: Logs de execução aparecem no terminal (stdout) e são retornados nas respostas da API.

---

## Pontos de Atenção

1. **`browser.py` é o arquivo mais crítico** (~1250 linhas). Alterações aqui afetam toda a execução de fluxos. Teste com cuidado.

2. **Locks de página**: Toda operação em uma página Playwright deve ser protegida por `acquire_lock(page_id)` / `release_lock(page_id)`. Workers de monitoramento e execução de fluxos competem pelo mesmo lock.

3. **Monitores não sobrevivem a reboot com status RUNNING**: Na inicialização, `load_monitors()` força todos os monitores para `STOPPED`. Isso é intencional — workers precisam ser reiniciados manualmente (ou pelo fluxo que os criou).

4. **`MonitorType` tem 8 valores, só `DOM` funciona**: Os tipos `NETWORK`, `CONSOLE`, `DOWNLOAD`, `REQUEST`, `RESPONSE`, `FILE`, `VARIABLE` estão definidos no enum mas não têm implementação no worker.

5. **Placeholders `config.py` e `storage.py`**: Não contêm código. Se precisar de configuração, use `.env` + `python-dotenv`.

6. **Perfis Chrome são persistentes**: Cookies, sessões, localStorage sobrevivem entre execuções. Isso é uma feature, mas pode causar comportamentos inesperados se o estado da sessão ficar inválido.

7. **Fluxos aceitam campos extras**: `FlowStep` tem `extra = "allow"`. Campos com typos (ex.: `seletor` vs `selector`) são aceitos silenciosamente. O sistema tenta ambos via fallback (`_required(..., fallback=...)`).

8. **Sem autenticação**: A API é totalmente aberta (localhost). Não há tokens, senhas ou controle de acesso. Isso é adequado para ferramenta local, mas deve ser considerado se for exposta em rede.

9. **O frontend faz polling, não WebSocket**: `app.js` consulta `/api/runtime` a cada 5s. `monitoring.html` consulta `/api/monitors` a cada 2s. Não há push em tempo real.

---

## Arquivos Mais Importantes

| Arquivo | Importância | Linhas (~) | Por quê |
|---|---|---|---|
| `app/core/browser.py` | **Crítica** | 1251 | Motor inteiro: navegador, perfis, fluxos, ações. |
| `app/api/routes.py` | **Alta** | ~530 | Todas as rotas REST. Interface pública do sistema. |
| `app/monitor/worker.py` | **Alta** | 419 | Loop de monitoramento e execução reativa. |
| `app/monitor/manager.py` | **Alta** | 141 | Gerenciamento do ciclo de vida dos monitores. |
| `app/monitor/storage.py` | **Média** | 99 | Persistência dos dados de monitoramento. |
| `app/models/schemas.py` | **Média** | 97 | Contratos da API. |
| `app/models/monitor.py` | **Média** | 35 | Definição do modelo Monitor. |
| `app/core/locks.py` | **Baixa** | 36 | Utilitário, estável. |
| `app/core/paths.py` | **Baixa** | 9 | Constantes, raramente muda. |
| `static/js/app.js` | **Alta** | 658 | Todo o frontend do dashboard. |
| `static/pages/monitoring.html` | **Alta** | 1368 | Frontend do centro de monitoramento (HTML+CSS+JS inline). |
| `main.py` | **Baixa** | ~3 | Apenas entry point do uvicorn. |
| `app/main.py` | **Alta** | ~126 | Lifespan, montagem da app, middleware. |