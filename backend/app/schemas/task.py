from pydantic import BaseModel
from enum import Enum
from typing import Optional

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

# Schema for creating a task
class TaskCreate(TaskBase):
    pass

# Schema for updating a task - all fields optional
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    details: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None

# Schema for reading/returning a Task
class Task(TaskBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True # Allows SQLAlchemy models to be returned as Pydantic Models
