# Python
import uuid
from urllib.parse import unquote

# FastAPI
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Cookie, HTTPException

# SQLALCHEMY
from sqlalchemy import select

# Database (postgresql)
from service.core.database import get_db, AsyncSessionLocal

# chatbot app models
from .models import MessageModel

# JWT
from service.auth.jwt_auth import get_user_via_access_token_async


# chatbot app router
router = APIRouter(prefix="/chatbot/api/v1", tags=["chatbot_api_v1"])

@router.websocket("/ws/{jwt_access_token}")
async def websocket_endpoint(websocket: WebSocket, jwt_access_token: str):
    await websocket.accept()

    jwt_access_token = unquote(jwt_access_token)

    if jwt_access_token is None:
        await websocket.send_text("NO TOKEN")
        await websocket.close(code=1008)
        return

    try:
        async with AsyncSessionLocal() as db:
            user = await get_user_via_access_token_async(jwt_access_token, db)
            messages = await db.execute(
                select(MessageModel)
                .where(MessageModel.user_id == user.id)
                .order_by(MessageModel.created_date)
            )
            for msg in messages:
                await websocket.send_text(f"{msg.role}: {msg.message}")

        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"پیام شما دریافت شد: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
    except HTTPException:
        await websocket.close(code=1008)