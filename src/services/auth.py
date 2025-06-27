from fastapi import Depends, HTTPException, WebSocketException
from fastapi_jwt_auth import AuthJWT
from starlette.websockets import WebSocket

from src.crud.auth import get_user_by_username
from src.databases.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.services.cookie import extract_token_from_cookie


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


async def get_current_user_ws(
    websocket: WebSocket,
    db: AsyncSession,
    auth: AuthJWT,
) -> User:
    """
    Raise WebSocketException(1008) on any auth failure.
    """
    token = extract_token_from_cookie(websocket)
    try:
        auth._token = token          # supply raw token
        auth.jwt_required()
        username = auth.get_jwt_subject()
    except Exception:
        raise WebSocketException(code=1008, reason="Invalid token")

    user = await get_user_by_username(db, username)
    if not user:
        raise WebSocketException(code=1008, reason="User not found")
    return user