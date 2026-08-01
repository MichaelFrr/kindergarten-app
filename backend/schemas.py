from pydantic import BaseModel, EmailStr
from sqlalchemy import Date
from datetime import date
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

class ChildCreate(BaseModel):
    name: str
    parent_email:EmailStr
    grade:str
    classroom_id:int
    membership_date: date


class ChildUpdate(BaseModel):
    name: Optional[str] = None
    parent_email: Optional[EmailStr] = None
    grade: Optional[str] = None
    classroom_id:Optional[int] = None
    membership_date: Optional[date] = None


class ChildResponse(BaseModel):
    uuid: UUID
    name: str
    parent_email:EmailStr
    grade:str
    classroom_id:int
    membership_date: date
    class Config:
        from_attributes = True


class ClassroomCreate(BaseModel):
    name:str
    capacity:int

class ClassroomUpdate(BaseModel):
    name:Optional[str] = None
    capacity:Optional[int] = None

class ClassroomResponse(BaseModel):
    id: int
    name:str
    capacity:int
    class Config:
        from_attributes = True

class LoginToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class Token(BaseModel):
    access_token: str
    token_type: str

class RefreshToken(BaseModel):
    refresh_token:str