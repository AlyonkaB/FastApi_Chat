from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.databases.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    chats = relationship("Chat", secondary="chat_users", back_populates="users")
    messages = relationship("Message", back_populates="sender")
