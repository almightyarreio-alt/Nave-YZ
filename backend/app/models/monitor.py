import uuid
from typing import Any, Optional
from pydantic import BaseModel, Field, PrivateAttr
from app.monitor.types import MonitorStatus

class Monitor(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    status: MonitorStatus = MonitorStatus.STOPPED
    type: str = "DOM"
    profile: str
    page_id: str
    frame_id: Optional[str] = None
    selector: str
    attribute: str = "textcontent"
    interval: float = 10.0
    timeout: float = 30.0
    started_at: Optional[str] = None
    last_check: Optional[str] = None
    last_change: Optional[str] = None
    last_error: Optional[str] = None
    last_value: Optional[str] = None
    verification_count: int = 0
    changes_count: int = 0
    save_snapshots: bool = False
    max_history: int = 100
    context: dict[str, Any] = Field(default_factory=dict)
    on_change: list[dict[str, Any]] = Field(default_factory=list)
    on_not_found: list[dict[str, Any]] = Field(default_factory=list)

    class Config:
        use_enum_values = True

    # Private runtime attributes that will not be serialized in JSON
    _running_task: Optional[Any] = PrivateAttr(default=None)
