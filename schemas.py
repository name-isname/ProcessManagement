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

class Process(ProcessBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # 更新为新的配置名

class Processwithlogs(Process):
    logs: list[str]

# 应该继承 ProcessBase 而不是 Process
class ProcessCreate(ProcessBase):
    pass

class ProcessUpdate(ProcessBase):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProcessStatus] = None
    priority: Optional[ProcessPriority] = None

class ProcessDelete(ProcessBase):
    pass

class LogBase(BaseModel):
    log_entry: str

class Log(LogBase):
    id: int
    process_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class LogCreate(LogBase):
    process_id: int
    log_entry: str

class LogUpdate(LogBase):
    log_entry: str

class LogDelete(LogBase):
    pass