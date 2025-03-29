from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional

class ProcessStatus(str, Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    PENDING = "pending"

class ProcessPriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ProcessCreate(BaseModel):
    name: str
    status: ProcessStatus
    priority: ProcessPriority
    details: Optional[str] = None

class Process(ProcessCreate):
    id: int
    created_at: datetime

    class Config:
        # orm_mode = True  # 旧版本写法
        from_attributes = True  # 新版本写法