from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

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
    hashed_password: str

    def model_post_init(self, __context):
        print(f"Created UserCreate instance with: {self.model_dump()}")

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True