from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    password: str


class CreateUser(UserBase):
    pass


class ReturnUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str
