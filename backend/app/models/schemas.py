from typing import Any

from pydantic import BaseModel, Field


class ProfileMetadata(BaseModel):
    name: str
    created_at: str
    last_used: str | None = None
    default: bool = False


class ProfileCreateRequest(BaseModel):
    name: str = Field(..., min_length=1)


class ProfileOpenRequest(BaseModel):
    name: str = Field(..., min_length=1)


class ProfileRenameRequest(BaseModel):
    new_name: str = Field(..., min_length=1)


class ProfileDefaultRequest(BaseModel):
    name: str = Field(..., min_length=1)


class ProfileOperationResponse(BaseModel):
    status: str = "success"
    profile: ProfileMetadata | None = None
    logs: list[dict[str, str]] = Field(default_factory=list)
    active_browsers: int | None = None
    url: str | None = None


class FlowStep(BaseModel):
    action: str
    url: str | None = None
    selector: str | None = None
    seletor: str | None = None
    value: str | None = None
    valor: str | None = None
    key: str | None = None
    tecla: str | None = None
    seconds: float | None = None
    segundos: float | None = None

    class Config:
        extra = "allow"


class FlowSaveRequest(BaseModel):
    name: str = Field(..., min_length=1)
    steps: list[dict[str, Any]] = Field(default_factory=list)

    class Config:
        extra = "allow"


class FlowSavedResponse(BaseModel):
    status: str
    flow: str
    path: str


class RunFlowRequest(BaseModel):
    profile: str = Field(..., min_length=1)
    flow: str = Field(..., min_length=1)


class LogEntry(BaseModel):
    timestamp: str
    tipo: str
    mensagem: str


class RunFlowResponse(BaseModel):
    status: str
    profile: str
    flow: str
    logs: list[LogEntry]
    active_browsers: int
    last_execution: dict[str, Any] | None = None


class ActionNavigate(BaseModel):
    url: str = Field(..., min_length=1)


class ActionFill(BaseModel):
    seletor: str = Field(..., min_length=1)
    valor: str = ""


class ActionClick(BaseModel):
    seletor: str = Field(..., min_length=1)
