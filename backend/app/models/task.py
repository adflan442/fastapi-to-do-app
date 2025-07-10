from sqlalchemy import ForeignKey, Column, String, Integer, Enum, func, DateTime
from sqlalchemy.orm import relationship

from app.core.db import Base
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
    __tablename__ = "tasks" # best practice: use lowercase table names

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    details = Column(String(2000), nullable=True)
    priority = Column(Enum(TaskPriority), default=TaskPriority.LOW)
    status = Column(Enum(TaskStatus), default=TaskStatus.CREATED)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="tasks")

    

