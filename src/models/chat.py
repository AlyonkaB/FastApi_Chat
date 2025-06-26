from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship

from src.databases.database import Base

chat_users = Table(
    "chat_users",
    Base.metadata,
    Column("chat_id", Integer, ForeignKey("chats.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
)


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    is_group = Column(Boolean, default=False)

    users = relationship("User", secondary=chat_users, back_populates="chats")
    messages = relationship("Message", back_populates="chat")
