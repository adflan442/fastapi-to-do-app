from sqlalchemy import ForeignKey, Column, String, Integer, Enum
from sqlalchemy.orm import relationship

from core.db import Base
from enum import Enum as PyEnum


class TaskPriority(str, PyEnum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH  = 'high'

class TaskStatus(str, PyEnum):
    CREATED = 'created'
    STARTED = 'started'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    details = Column(String(2000), nullable=True)
    priority = Column(Enum(TaskPriority), default=TaskPriority.LOW)
    status = Column(Enum(TaskStatus), default=TaskStatus.CREATED)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="tasks")

    

