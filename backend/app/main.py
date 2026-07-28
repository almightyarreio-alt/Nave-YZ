import asyncio
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import legacy_router, router
from app.core.browser import BrowserManager
from app.monitor.manager import monitor_manager

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

BASE_DIR = Path(__file__).resolve().parents[1]
INDEX_FILE = BASE_DIR / "index.html"
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

browser_manager = BrowserManager(BASE_DIR)


@asynccontextmanager
async def lifespan(app: FastAPI):
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    app.state.base_dir = BASE_DIR
    app.state.browser_manager = browser_manager
    app.state.monitor_manager = monitor_manager
    await browser_manager.start()
    
    # Initialize monitor manager
    monitor_manager.initialize(BASE_DIR, browser_manager)
    
    try:
        yield
    finally:
        # Stop background tasks
        for monitor_id in list(monitor_manager.tasks.keys()):
            await monitor_manager.stop_task(monitor_id)
        await browser_manager.stop()


app = FastAPI(
    title="Navyauto MVP",
    description="Orquestrador RPA local-first com FastAPI, Playwright e Chrome persistente.",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Civilização React (Vite)
        "http://localhost:3000",  # Outras origens se necessário
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.base_dir = BASE_DIR
app.state.browser_manager = browser_manager
app.state.monitor_manager = monitor_manager

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.include_router(router, prefix="/api")
app.include_router(legacy_router)


@app.get("/", response_class=HTMLResponse)
async def dashboard() -> str:
    if not INDEX_FILE.exists():
        raise HTTPException(status_code=404, detail="index.html nao encontrado.")
    return INDEX_FILE.read_text(encoding="utf-8")
