from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from src.crud.auth import get_user_by_username
from src.databases.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


async def get_current_user(
    Authorize: AuthJWT = Depends(), db: AsyncSession = Depends(get_db)
):
    try:
        print(f"Cookies: {Authorize.get_raw_jwt()}")
        Authorize.jwt_required()
        current_user_username = Authorize.get_jwt_subject()
        db_user = await get_user_by_username(db, current_user_username)

        if not db_user:
            raise HTTPException(status_code=401, detail="User not found")

        return db_user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid or expired token {e}")
