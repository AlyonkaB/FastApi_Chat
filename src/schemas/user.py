import re

from pydantic import BaseModel, EmailStr, validator
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserList(UserBase):
    id: int


class UserCreate(UserBase):
    hashed_password: str

    @validator("hashed_password")
    def check_password(cls, value):
        if not value:
            raise ValueError("Password cannot be empty")

        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")

        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r"[\W_]", value):
            raise ValueError("Password must contain at least one special character")

        return value


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    hashed_password: Optional[str] = None

    class Config:
        orm_mode = True
