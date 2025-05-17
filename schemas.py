from pydantic import BaseModel
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    user = "user"
    admin = "admin"

class UserCreate(BaseModel):
    name: str
    age: int
    role: RoleEnum

class UserUpdate(BaseModel):
    name: Optional[str] | None
    role: Optional[RoleEnum] | None
    age: Optional[int] | None

class UserGet(BaseModel):
    name: str
    age: int

class UserDelete(BaseModel):
    id: int

class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    role: str

    class Config:
        from_attributes = True