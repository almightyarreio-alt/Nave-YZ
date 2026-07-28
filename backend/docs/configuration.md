# Configuração

Documentação de variáveis de ambiente, arquivos de configuração, configurações padrão e dependências externas.

---

## Variáveis de Ambiente

Carregadas via `python-dotenv` no arquivo `.env` na raiz do projeto.

**Arquivo**: `.env` (não versionado no Git, listado no `.gitignore`).

### Variáveis utilizadas

As variáveis de ambiente são carregadas no `BrowserManager` e ficam disponíveis como placeholders `{NOME_VAR}` nos fluxos JSON.

| Variável | Uso típico | Exemplo |
|---|---|---|
| `LICITANET_CRETA_USER` | Usuário para login no portal Licitanet | `usuario@exemplo.com` |
| `LICITANET_CRETA_PASS` | Senha para login | `senha123` |
| Outras credenciais | Conforme necessidade dos fluxos | `{API_KEY}`, `{WEBHOOK_URL}` |

**Nota**: As variáveis não têm nomes fixos — qualquer chave no `.env` pode ser referenciada como `{CHAVE}` nos passos de fluxo.

### Exemplo de `.env`

```env
LICITANET_CRETA_USER=meu_usuario
LICITANET_CRETA_PASS=minha_senha
WEBHOOK_DISCORD=https://discord.com/api/webhooks/...
```

### Como são carregadas

Em `app/core/browser.py`, no método `start()`:

```python
from dotenv import load_dotenv
load_dotenv()
# ...
self._variables = dict(os.environ)
```

Todas as variáveis do ambiente (incluindo as do `.env`) são copiadas para `self._variables` do `BrowserManager`.

---

## Arquivos de Configuração

Não há arquivos de configuração dedicados (YAML, TOML, INI, etc.). O sistema usa:

| Mecanismo | Arquivo/Local | Propósito |
|---|---|---|
| `.env` | Raiz do projeto | Credenciais e variáveis sensíveis |
| `requirements.txt` | Raiz do projeto | Dependências Python |
| `Navyauto.spec` | Raiz do projeto | Configuração de empacotamento PyInstaller |
| `flows/*.json` | `flows/` | Definições de automação (declarativas) |
| `data/monitors/<id>/current.json` | `data/monitors/` | Estado persistente dos monitores |
| `profiles/<name>/` | `profiles/` | Perfis Chrome (gerenciados pelo Playwright) |

---

## Configurações Padrão (Hardcoded)

Valores definidos diretamente no código, sem mecanismo externo de configuração:

| Configuração | Valor | Local |
|---|---|---|
| Host do servidor | `127.0.0.1` | `main.py` → `uvicorn.run(..., host="127.0.0.1")` |
| Porta do servidor | `8000` | `main.py` → `uvicorn.run(..., port=8000)` |
| Navegador | Chromium (Chrome) | `BrowserManager.start()` → `playwright.chromium.launch(headless=False)` |
| Headless | `False` (sempre com UI) | `browser.py`, linha ~88 |
| Perfil padrão (default) | `"Perfil Principal"` | `BrowserManager.start()` — criado se `profiles/` estiver vazio |
| Diretório de perfis | `ROOT / "profiles"` | `app/core/paths.py` |
| Diretório de fluxos | `ROOT / "flows"` | `app/core/paths.py` |
| Diretório de dados | `ROOT / "data"` | `app/core/paths.py` |
| Status inicial de monitores | `STOPPED` (sempre no boot) | `MonitorManager.load_monitors()` |
| Timeout padrão de monitor | `30.0` segundos | `Monitor.timeout` default |
| Intervalo padrão de monitor | `10.0` segundos | `Monitor.interval` default |
| Atributo padrão de monitor | `"textcontent"` | `Monitor.attribute` default |
| Tipo padrão de monitor | `"DOM"` | `Monitor.type` default |
| Histórico máximo de monitor | `100` entradas | `Monitor.max_history` default |
| Snapshots | `False` (não captura por padrão) | `Monitor.save_snapshots` default |
| Polling do dashboard | 5 segundos | `static/js/app.js` → `setInterval(loadRuntime, 5000)` |
| Polling do centro de monitoramento | 2 segundos | `static/pages/monitoring.html` → `setInterval(fetchMonitors, 2000)` |
| Timeout do seletor no worker | `min(5000, monitor.timeout * 1000)` ms | `app/monitor/worker.py`, linha 209 |

---

## Dependências Externas

### Python (requirements.txt)

| Pacote | Versão (especificada) | Finalidade |
|---|---|---|
| `fastapi` | *latest* | Framework web |
| `uvicorn` | *latest* | Servidor ASGI |
| `playwright` | *latest* | Automação de navegador |
| `pydantic` | `>=2.0` | Validação de dados |
| `python-dotenv` | *latest* | Carregar `.env` |
| `beautifulsoup4` | *latest* | Parsing HTML (monitoramento) |
| `requests` | *latest* | Notificações webhook |

### Infraestrutura

| Dependência | Tipo | Necessidade |
|---|---|---|
| **Google Chrome** (ou Chromium) | Navegador instalado | O Playwright usa o Chrome instalado no sistema. Deve estar presente. |
| **Playwright Browsers** | Binários | `playwright install chromium` instala o binário do Chromium. |

### Frontend (CDN, sem instalação local)

| Dependência | URL CDN | Finalidade |
|---|---|---|
| **Tailwind CSS** | `https://cdn.tailwindcss.com` | Framework CSS utilitário |
| **Lucide Icons** | `https://unpkg.com/lucide@latest` | Biblioteca de ícones |
| **Google Fonts** (Outfit + JetBrains Mono) | `https://fonts.googleapis.com` | Fontes do dashboard |

### Serviços Externos (opcionais)

| Serviço | Uso | Onde |
|---|---|---|
| **Webhook HTTP** (Discord, Slack, etc.) | Notificações da ação `notify` e de `on_change`/`on_not_found` | `app/core/browser.py` (linha ~1218), `app/monitor/worker.py` |
| **Sites alvo** (Licitanet, etc.) | Páginas automatizadas pelos fluxos | Definidos nos JSON de `flows/` |

---

## Persistência de Dados

| O que | Onde | Formato |
|---|---|---|
| Perfis Chrome (cookies, localStorage, cache) | `profiles/<nome>/` | Diretório Chrome padrão (gerenciado pelo Playwright) |
| Estado de monitores | `data/monitors/<uuid>/current.json` | JSON |
| Histórico de verificações | `data/monitors/<uuid>/history.jsonl` | JSON Lines (um objeto por linha) |
| Snapshots de tela | `data/monitors/<uuid>/snapshots/*.png` | PNG |
| Logs de execução | `data/logs/` (diretório existe, mas logs em disco não estão implementados — apenas em memória/API) | — |
| Cache | `data/cache/` (diretório existe, sem uso ativo no código) | — |