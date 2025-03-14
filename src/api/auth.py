from fastapi import APIRouter, HTTPException, Depends, Response
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
    user: UserLogin, response: Response, Authorize: AuthJWT = Depends(), db: AsyncSession = Depends(get_db),
):
    try:
        db_user = await get_user_by_username(db, user.username)
        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )

        access_token = Authorize.create_access_token(subject=db_user.username)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,  # You may want to use this for HTTPS connections
            samesite="Strict"  # Optional, helps prevent CSRF attacks
        )
        return {"access_token": access_token}
    except AuthJWTException as e:
        raise HTTPException(status_code=401, detail=f"Error JWT: {str(e)}")
