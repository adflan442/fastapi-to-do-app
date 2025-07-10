from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime

# Match Enums from the Model
class TaskStatus(str, Enum):
    CREATED = "created"
    STARTED = "started"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskPriority(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

# Base Schema for shared fields
class TaskBase(BaseModel):
    title: str
    details: Optional[str] = None
    status: TaskStatus = TaskStatus.CREATED
    priority: Optional[TaskPriority] = TaskPriority.LOW

# Schema for reading/returning a Task
class TaskResponse(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True # Allows SQLAlchemy models to be returned as Pydantic Models

# Schema for creating a task
class TaskCreate(TaskBase):
    pass # Inherits all TaskBase fields - can update with more later

# Schema for updating a task - all fields optional
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    details: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None

