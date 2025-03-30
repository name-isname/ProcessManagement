from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional

class ProcessStatus(str, Enum):
    RUNNING = "运行中"
    STOPPED = "停止"
    PENDING = "等待中"

class ProcessPriority(str, Enum):
    HIGH = "高"
    MEDIUM = "中"
    LOW = "低"

class ProcessBase(BaseModel):
    id : int

class Process(ProcessBase):
    name: str
    description: Optional[str] = None
    status: ProcessStatus
    priority: ProcessPriority
    created_at: datetime

class Processwithlogs(Process):
    logs: list[str]

class ProcessCreate(Process):
    pass

class ProcessUpdate(ProcessBase):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProcessStatus] = None
    priority: Optional[ProcessPriority] = None

class ProcessDelete(ProcessBase):
    pass

class LogBase(BaseModel):
    id: int

class Log(LogBase):
    process_id: int
    log_entry: str
    created_at: datetime

class LogCreate(LogBase):
    process_id: int
    log_entry: str

class LogUpdate(LogBase):
    log_entry: str

class LogDelete(LogBase):
    pass