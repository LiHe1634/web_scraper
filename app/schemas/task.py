from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from app.models.task import TaskStatus, TaskPriority

class TaskBase(BaseModel):
    name: str
    url: str
    schedule: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    config: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, str]] = None
    cookies: Optional[Dict[str, str]] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    name: Optional[str] = None
    url: Optional[str] = None
    status: Optional[TaskStatus] = None
    retry_count: Optional[int] = None
    error_message: Optional[str] = None

class TaskInDBBase(TaskBase):
    id: int
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    last_run: Optional[datetime]
    next_run: Optional[datetime]
    retry_count: int
    user_id: int

    class Config:
        orm_mode = True

class Task(TaskInDBBase):
    pass

class TaskInDB(TaskInDBBase):
    pass
