# app/ws/ws_manager.py
from typing import Dict
from fastapi import WebSocket


class ConnectionManager:
    class ConnectionManager:
        def __init__(self):
            self.active_connections: Dict[str, WebSocket] = {}

        def register(self, session_id: str, websocket: WebSocket):
            self.active_connections[session_id] = websocket

        def disconnect(self, session_id: str):
            self.active_connections.pop(session_id, None)

        async def send_json(self, session_id: str, data: dict):
            websocket = self.active_connections.get(session_id)
            if websocket:
                await websocket.send_json(data)

        async def send_text(self, session_id: str, message: str):
            websocket = self.active_connections.get(session_id)
            if websocket:
                await websocket.send_text(message)