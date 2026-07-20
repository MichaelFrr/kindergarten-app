from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    uuid: UUID
    first_name: str
    email: str
    role: str

    class Config:
        from_attributes = True
