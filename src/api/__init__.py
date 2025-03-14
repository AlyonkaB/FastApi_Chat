from fastapi import APIRouter
from src.api.user import router as user_router
from src.api.auth import router as auth_router

main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(auth_router)
