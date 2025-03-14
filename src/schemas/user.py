from pydantic import BaseModel, EmailStr, validator
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserList(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    hashed_password: str

    @validator("hashed_password")
    def check_password(cls, value):
        if not value:
            raise ValueError("Password cannot be empty")
        return value


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    hashed_password: Optional[str] = None

    class Config:
        orm_mode = True
