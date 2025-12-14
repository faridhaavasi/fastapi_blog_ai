# FastAPI
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

# SQLALCHEMY
from sqlalchemy.orm import Session
from sqlalchemy import select

# Database (postgresql)
from service.core.database import get_db, AsyncSessionLocal

# Database (mongodb)
from service.core.database import mongo_db

# chatbot app schemas
from .schemas import (
    GetAllMassageSchema,
    UserSendMassageSchema,
)

# chatbot app models
from .models import MessageModel

# JWT
from service.auth.jwt_auth import get_user_via_access_token

# chatbot ws manager
from .ws_manager import ConnectionManager

# openai
from service.AI.AI_func import stream_chat_response


# chatbot app router
router = APIRouter(prefix="/chatbot/api/v1", tags=["chatbot_api_v1"])

# chatbot app ws manager
manager = ConnectionManager()



@router.websocket("/ws/chat")
async def chatbot_ws(websocket: WebSocket, user_id: int):
    session_id = str(uuid.uuid4())
    await manager.connect(session_id, websocket)

    async with AsyncSessionLocal() as db:
        try:
            # 1️⃣ ارسال history موقع connect
            result = await db.execute(
                select(MessageModel)
                .where(MessageModel.user_id == user_id)
                .order_by(MessageModel.created_date)
                .limit(50)
            )
            history = result.scalars().all()

            for msg in history:
                await manager.send_json(session_id, {
                    "type": "history",
                    "role": msg.role,
                    "message": msg.message,
                    "created_date": msg.created_date.isoformat()
                })

            # 2️⃣ loop اصلی چت
            while True:
                user_message = await websocket.receive_text()

                # ذخیره پیام کاربر
                db.add(MessageModel(
                    user_id=user_id,
                    role="user",
                    message=user_message
                ))
                await db.commit()

                # ساخت context برای OpenAI
                context = [
                    {"role": msg.role, "content": msg.message}
                    for msg in history
                ]
                context.append({"role": "user", "content": user_message})

                full_response = ""

                await manager.send_json(session_id, {"type": "start"})

                async for token in stream_chat_response(context):
                    full_response += token
                    await manager.send_json(session_id, {
                        "type": "stream",
                        "token": token
                    })

                await manager.send_json(session_id, {"type": "end"})

                # ذخیره پاسخ AI
                db.add(MessageModel(
                    user_id=user_id,
                    role="assistant",
                    message=full_response
                ))
                await db.commit()

                # history رو به‌روز کن (برای پیام بعدی)
                history.append(
                    MessageModel(
                        role="user",
                        message=user_message
                    )
                )
                history.append(
                    MessageModel(
                        role="assistant",
                        message=full_response
                    )
                )

        except WebSocketDisconnect:
            manager.disconnect(session_id)

































