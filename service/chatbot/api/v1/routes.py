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

# AI
from service.AI.AI_func import stream_chat_response


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
            user_message = await websocket.receive_text()

            await websocket.send_text(f"you: {user_message}")

            new_user_message = MessageModel(user_id=user.id, role='user', message=user_message)

            db.add(new_user_message)
            db.commit()

            ai_message = stream_chat_response(user_message)

            new_ai_message = MessageModel(user_id=user.id, role='ai', message=ai_message)

            db.add(new_ai_message)
            db.commit()

            await websocket.send_text(f"AI: {ai_message}")
    except WebSocketDisconnect:
        print("Client disconnected")
    except HTTPException:
        await websocket.close(code=1008)