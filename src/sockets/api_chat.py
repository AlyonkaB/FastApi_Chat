from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect, WebSocket

from src.databases.database import get_db
from src.services.auth import get_current_user_ws
from src.sockets.manager import manager

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


@router.get("/")
async def get():
    return HTMLResponse(html)

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_db),
    auth: AuthJWT = Depends(),        # ⬅ here
):
    await websocket.accept()

    user = await get_current_user_ws(websocket, db)

    await manager.connect(websocket, user.username)
    await manager.broadcast(f"🟢 {user.username} joined")

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{user.username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"🔴 {user.username} left")



