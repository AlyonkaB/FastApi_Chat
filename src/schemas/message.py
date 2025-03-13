from pydantic import BaseModel, Field
from datetime import datetime


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)


class MessageResponse(BaseModel):
    id: int
    user_id: int
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True
