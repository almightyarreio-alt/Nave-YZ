import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from app.models.monitor import Monitor
from app.monitor.types import MonitorStatus
from app.monitor.storage import MonitorStorage
from app.monitor.worker import monitor_worker, run_on_change, run_on_not_found

class MonitorManager:
    def __init__(self, base_dir: Optional[Path] = None, browser_manager: Optional[Any] = None):
        self.base_dir = base_dir
        self.browser_manager = browser_manager
        self.storage = MonitorStorage(base_dir) if base_dir else None
        self.monitors: Dict[str, Monitor] = {}
        self.tasks: Dict[str, asyncio.Task] = {}

    def initialize(self, base_dir: Path, browser_manager: Any) -> None:
        """Initializes the manager with dependencies after startup."""
        self.base_dir = Path(base_dir)
        self.browser_manager = browser_manager
        self.storage = MonitorStorage(self.base_dir)
        self.load_monitors()

    def load_monitors(self) -> None:
        """Loads all monitor configurations and rebuilds objects in STOPPED state."""
        if not self.storage:
            return
        monitors_data = self.storage.load_all_monitors()
        for data in monitors_data:
            try:
                # Reboot rule: all monitors start as STOPPED on initialization
                data["status"] = MonitorStatus.STOPPED
                monitor = Monitor(**data)
                self.monitors[monitor.id] = monitor
            except Exception as e:
                print(f"Erro ao carregar monitor salvo: {e}")

    def list_monitors(self) -> List[Monitor]:
        return list(self.monitors.values())

    def get_monitor(self, monitor_id: str) -> Optional[Monitor]:
        return self.monitors.get(monitor_id)

    async def register_monitor(self, **kwargs) -> Monitor:
        """Registers a new monitor, saves its current.json, and returns it."""
        if not self.storage:
            raise RuntimeError("MonitorManager não inicializado com storage.")
            
        monitor = Monitor(**kwargs)
        self.monitors[monitor.id] = monitor
        self.storage.save_current(monitor)
        return monitor

    async def start_monitor(self, monitor_id: str) -> None:
        """Starts a monitor in background (idempotent operation)."""
        monitor = self.get_monitor(monitor_id)
        if not monitor:
            raise ValueError("Monitor não encontrado.")

        if monitor.status == MonitorStatus.RUNNING:
            return  # Idempotente: evita iniciar duas tasks para o mesmo monitor

        # Stop existing background task if any (should not exist, but let's be safe)
        await self.stop_task(monitor_id)

        monitor.status = MonitorStatus.RUNNING
        monitor.started_at = monitor.started_at or datetime.now().replace(microsecond=0).isoformat()
        self.storage.save_current(monitor)

        # Start background worker task
        task = asyncio.create_task(monitor_worker(monitor_id, self))
        self.tasks[monitor_id] = task

    async def pause_monitor(self, monitor_id: str) -> None:
        """Pauses a running monitor."""
        monitor = self.get_monitor(monitor_id)
        if not monitor:
            raise ValueError("Monitor não encontrado.")

        await self.stop_task(monitor_id)
        monitor.status = MonitorStatus.PAUSED
        self.storage.save_current(monitor)

    async def stop_monitor(self, monitor_id: str) -> None:
        """Stops a monitor."""
        monitor = self.get_monitor(monitor_id)
        if not monitor:
            raise ValueError("Monitor não encontrado.")

        await self.stop_task(monitor_id)
        monitor.status = MonitorStatus.STOPPED
        self.storage.save_current(monitor)

    async def remove_monitor(self, monitor_id: str) -> None:
        """Removes a monitor from configuration. Errors if the monitor is currently running."""
        monitor = self.get_monitor(monitor_id)
        if not monitor:
            raise ValueError("Monitor não encontrado.")

        if monitor.status == MonitorStatus.RUNNING:
            raise ValueError("Não é possível remover um monitor em execução. Pause ou pare o monitor primeiro.")

        await self.stop_task(monitor_id)
        self.monitors.pop(monitor_id, None)
        if self.storage:
            self.storage.delete_monitor_data(monitor_id)

    async def stop_task(self, monitor_id: str) -> None:
        """Cancels and awaits the background task of a monitor."""
        task = self.tasks.pop(monitor_id, None)
        if task and not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    def trigger_on_change(self, monitor_id: str, steps: List[dict]) -> None:
        """Spawns an independent background task to run the on_change flow."""
        asyncio.create_task(run_on_change(monitor_id, steps, self))

    def trigger_on_not_found(self, monitor_id: str, steps: List[dict]) -> None:
        """Spawns an independent background task to run the on_not_found flow."""
        asyncio.create_task(run_on_not_found(monitor_id, steps, self))

    async def handle_page_closed(self, page_id: str) -> None:
        """Callback triggered when a page is closed. Transitions all related monitors to ERROR status."""
        for monitor in list(self.monitors.values()):
            if monitor.page_id == page_id:
                # Cancel task
                await self.stop_task(monitor.id)
                
                # Update status
                monitor.status = MonitorStatus.ERROR
                monitor.last_error = "Página associada foi encerrada no navegador."
                if self.storage:
                    self.storage.save_current(monitor)

# Global singleton instance
monitor_manager = MonitorManager()
