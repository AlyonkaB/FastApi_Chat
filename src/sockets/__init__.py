from fastapi import APIRouter
from src.sockets.api_chat import router as user_router


socket_router = APIRouter()

socket_router.include_router(user_router)
