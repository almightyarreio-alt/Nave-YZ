from enum import Enum

class MonitorStatus(str, Enum):
    STOPPED = "STOPPED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    ERROR = "ERROR"
    NOT_FOUND = "NOT_FOUND"

class MonitorType(str, Enum):
    DOM = "DOM"
    NETWORK = "NETWORK"
    CONSOLE = "CONSOLE"
    DOWNLOAD = "DOWNLOAD"
    REQUEST = "REQUEST"
    RESPONSE = "RESPONSE"
    FILE = "FILE"
    VARIABLE = "VARIABLE"
