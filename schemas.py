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
    name: str
    description: Optional[str] = None
    status: ProcessStatus
    priority: ProcessPriority

    class Config:
        from_attributes = True

class Process(ProcessBase):
    id: int
    created_at: datetime

# 应该继承 ProcessBase 而不是 Process
class ProcessCreate(ProcessBase):
    pass

class ProcessUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProcessStatus] = None
    priority: Optional[ProcessPriority] = None

    class Config:
        from_attributes = True

class LogBase(BaseModel):
    log_entry: str
    
    class Config:
        from_attributes = True

class Log(LogBase):
    id: int
    process_id: int
    created_at: datetime

class LogCreate(LogBase):
    pass

class LogUpdate(LogBase):
    pass

class ProcessWithLogs(Process):
    logs: list[Log]

    class Config:
        from_attributes = True