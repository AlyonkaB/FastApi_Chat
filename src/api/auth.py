from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from src.crud.auth import get_user_by_username, verify_password
from src.databases.database import get_db
from src.schemas.auth import UserLogin, Settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


@AuthJWT.load_config
def get_config():
    return Settings()


@router.post("/login")
async def login(
    user: UserLogin, Authorize: AuthJWT = Depends(), db: AsyncSession = Depends(get_db)
):
    try:
        db_user = await get_user_by_username(db, user.username)
        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(
                status_code=400, detail="Невірне ім'я користувача або пароль"
            )

        access_token = Authorize.create_access_token(subject=db_user.username)
        return {"access_token": access_token}
    except AuthJWTException as e:
        raise HTTPException(status_code=401, detail=f"Помилка JWT: {str(e)}")
