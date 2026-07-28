import json
import os
import shutil
from pathlib import Path
from typing import Any, List, Optional

class MonitorStorage:
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.monitors_dir = self.base_dir / "data" / "monitors"
        self.monitors_dir.mkdir(parents=True, exist_ok=True)

    def _get_monitor_path(self, monitor_id: str) -> Path:
        path = self.monitors_dir / monitor_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def save_current(self, monitor: Any) -> None:
        path = self._get_monitor_path(monitor.id)
        current_file = path / "current.json"
        
        # Convert Monitor model to dict
        data = monitor.model_dump() if hasattr(monitor, "model_dump") else monitor.dict()
        
        # Write to current.json, overwriting the file
        current_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def load_all_monitors(self) -> List[dict]:
        monitors = []
        if not self.monitors_dir.exists():
            return monitors
        for m_dir in self.monitors_dir.iterdir():
            if m_dir.is_dir() and not m_dir.name.startswith("."):
                current_file = m_dir / "current.json"
                if current_file.exists():
                    try:
                        data = json.loads(current_file.read_text(encoding="utf-8"))
                        monitors.append(data)
                    except Exception as e:
                        print(f"Error loading current.json for monitor {m_dir.name}: {e}")
        return monitors

    def delete_monitor_data(self, monitor_id: str) -> None:
        path = self.monitors_dir / monitor_id
        if path.exists() and path.is_dir():
            shutil.rmtree(path)

    def append_history(self, monitor_id: str, entry: dict, max_history: int) -> None:
        path = self._get_monitor_path(monitor_id)
        history_file = path / "history.jsonl"
        
        # Append entry
        line = json.dumps(entry, ensure_ascii=False) + "\n"
        with open(history_file, "a", encoding="utf-8") as f:
            f.write(line)
            
        # Rotate if exceeds max_history
        if max_history > 0:
            try:
                lines = history_file.read_text(encoding="utf-8").splitlines()
                if len(lines) > max_history:
                    # Keep the last max_history lines
                    rotated_lines = lines[-max_history:]
                    history_file.write_text("\n".join(rotated_lines) + "\n", encoding="utf-8")
            except Exception as e:
                print(f"Error rotating history file: {e}")

    def get_history(self, monitor_id: str) -> List[dict]:
        path = self._get_monitor_path(monitor_id)
        history_file = path / "history.jsonl"
        history = []
        if history_file.exists():
            try:
                for line in history_file.read_text(encoding="utf-8").splitlines():
                    if line.strip():
                        history.append(json.loads(line))
            except Exception as e:
                print(f"Error reading history.jsonl: {e}")
        return history

    def save_snapshot(self, monitor_id: str, file_name: str, content: bytes) -> str:
        path = self._get_monitor_path(monitor_id)
        snapshots_dir = path / "snapshots"
        snapshots_dir.mkdir(parents=True, exist_ok=True)
        snapshot_file = snapshots_dir / file_name
        snapshot_file.write_bytes(content)
        return file_name

    def get_snapshot_path(self, monitor_id: str, file_name: str) -> Optional[Path]:
        path = self.monitors_dir / monitor_id / "snapshots" / file_name
        if path.exists() and path.is_file():
            return path
        return None

    def get_snapshots_list(self, monitor_id: str) -> List[str]:
        snapshots_dir = self.monitors_dir / monitor_id / "snapshots"
        if snapshots_dir.exists() and snapshots_dir.is_dir():
            return sorted([f.name for f in snapshots_dir.iterdir() if f.is_file()])
        return []
