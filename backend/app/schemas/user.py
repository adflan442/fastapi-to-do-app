from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional, Any

# User Role Schema
class UserRole(str, Enum):
    GENERAL = 'general'
    PREMIUM = 'premium'
    ADMIN = 'admin'

# Shared Properties
class UserBase(BaseModel):
    email: EmailStr
    username: str
    firstname: str
    lastname: str
    role: UserRole = UserRole.GENERAL


class UserCreate(UserBase):
    password: str

    def model_post_init(self, __context: Any) -> None:
        print(f"Created UserCreate instance with: {self.model_dump()}")

class UserRead(UserBase):
    id: int
    username: str
    firstname: str
    lastname: str
    email: str
    role: Optional[str] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    role: Optional[str] = None

class UserRegister(BaseModel):
    email: EmailStr
    username: str
    firstname: str
    lastname: str
    role: Optional[UserRole] = UserRole.GENERAL
    password: str

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str

