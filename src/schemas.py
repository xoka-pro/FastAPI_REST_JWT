from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional


class ContactResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    other_info: Optional[str]
    created_at: date
    updated_at: date

    class Config:
        orm_mode = True


class BirthdayResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    birthday: date


class UserModel(BaseModel):
    username: str = Field(min_length=6, max_length=12)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar: str

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
