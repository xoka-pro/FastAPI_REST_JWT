from pydantic import BaseModel, EmailStr
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
