from fastapi import Depends, HTTPException, WebSocketException
from fastapi_jwt_auth import AuthJWT
from starlette import status
from starlette.websockets import WebSocket

from src.crud.auth import get_user_by_username
from src.databases.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User


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
    db: AsyncSession = Depends(get_db),
) -> User:
    # 1️⃣ дістаємо cookie
    cookies = websocket.headers.get("cookie")
    if not cookies:
        raise WebSocketException(status.WS_1008_POLICY_VIOLATION, "No cookies")

    token = None
    for item in cookies.split(";"):
        name, _, value = item.strip().partition("=")
        if name == "access_token_cookie":
            token = value
            break

    if not token:
        raise WebSocketException(status.WS_1008_POLICY_VIOLATION, "No access token")

    # 2️⃣ валідуємо JWT
    authorize = AuthJWT()
    try:
        authorize._token = token  # передаємо токен вручну
        authorize.jwt_required()
        username = authorize.get_jwt_subject()

        user = await get_user_by_username(db, username)
        if not user:
            raise WebSocketException(status.WS_1008_POLICY_VIOLATION, "User not found")
        return user
    except Exception:
        raise WebSocketException(status.WS_1008_POLICY_VIOLATION, "Invalid token")
