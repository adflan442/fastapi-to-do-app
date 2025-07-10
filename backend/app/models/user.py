from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.orm import relationship
from app.core.db import Base
import enum


class UserRole(enum.Enum):
    GENERAL = 'general'
    PREMIUM = 'premium'
    ADMIN = 'admin'

class User(Base):
    __tablename__ = "users"  # best practice: use lowercase table names

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    firstname = Column(String(50), unique=False, nullable=False)
    lastname = Column(String(50), unique=False, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.GENERAL)

    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")