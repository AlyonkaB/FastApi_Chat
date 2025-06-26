from fastapi import APIRouter, WebSocketException, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect, WebSocket

from src.crud.auth import get_user_by_username
from src.databases.database import get_db
from src.models import User
from src.services.auth import get_current_user_ws

router = APIRouter(prefix="/chat", tags=["Chat"])

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
    var client_id = Date.now();
    document.querySelector("#ws-id").textContent = client_id;

    // Токен із cookie — витягнемо вручну
    const getCookie = (name) => {
        const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return match ? match[2] : null;
    }

    const token = getCookie('access_token_cookie');

    // 🔁 Додаємо токен у query-параметр
    var ws = new WebSocket("ws://localhost:8000/chat/ws");

    ws.onmessage = function(event) {
        var messages = document.getElementById('messages');
        var message = document.createElement('li');
        var content = document.createTextNode(event.data);
        message.appendChild(content);
        messages.appendChild(message);
    };

    function sendMessage(event) {
        var input = document.getElementById("messageText");
        ws.send(input.value);
        input.value = '';
        event.preventDefault();
    }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket, username: str):
        self.active_connections[websocket] = username

    def disconnect(self, websocket: WebSocket):
        self.active_connections.pop(websocket, None)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(connection)


manager = ConnectionManager()


@router.get("/")
async def get():
    return HTMLResponse(html)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    await websocket.accept()

    cookie_header = websocket.headers.get("cookie")
    token = None
    if cookie_header:
        for cookie in cookie_header.split(";"):
            name, _, value = cookie.strip().partition("=")
            if name == "access_token_cookie":
                token = value
                break

    if not token:
        raise WebSocketException(code=1008, reason="Missing token")

    authorize = AuthJWT()
    try:
        authorize._token = token
        authorize.jwt_required()
        username = authorize.get_jwt_subject()
        user = await get_user_by_username(db, username)
        if not user:
            raise WebSocketException(code=1008, reason="User not found")
    except Exception:
        raise WebSocketException(code=1008, reason="Invalid token")

    await manager.connect(websocket, user.username)
    await manager.broadcast(f"🟢 {user.username} joined")

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{user.username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"🔴 {user.username} left")
