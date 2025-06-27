from fastapi import WebSocketException
from starlette.websockets import WebSocket


def extract_token_from_cookie(websocket: WebSocket) -> str:
    cookie_header = websocket.headers.get("cookie")
    token = None
    for part in cookie_header.split(";"):
        name, _, token = part.strip().partition("=")
        if name == "access_token_cookie":
            return token
    raise WebSocketException(code=1008, reason="Missing token")
