from fastapi import FastAPI
from src.api import main_router
from src.sockets import socket_router

app = FastAPI()
app.include_router(main_router)
app.include_router(socket_router)
