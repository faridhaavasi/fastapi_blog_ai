# Python
import uuid

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



@router.websocket("/chatbot")
async def chatbot_ws(websocket: WebSocket):
    session_id = str(uuid.uuid4())
    # 1️⃣ اول accept
    await websocket.accept()

    # 2️⃣ AUTH از cookie
    token = websocket.cookies.get("jwt_access_token")
    if not token:
        await websocket.close(code=1008)
        return

    try:
        user = get_user_via_access_token(token)
    except Exception:
        await websocket.close(code=1008)
        return

    # 3️⃣ فقط بعد از auth، ثبت connection
    manager.active_connections[session_id] = websocket

    try:
        async with AsyncSessionLocal() as db:

            # 4️⃣ load history
            result = await db.execute(
                select(MessageModel)
                .where(MessageModel.user_id == user.id)
                .order_by(MessageModel.created_date)
                .limit(50)
            )
            history = result.scalars().all()

            for msg in history:
                await manager.send_json(session_id, {
                    "role": msg.role,
                    "message": msg.message,
                    "created_date": msg.created_date.isoformat()
                })

            # 5️⃣ loop اصلی چت
            while True:
                user_message = await websocket.receive_text()

                # ذخیره پیام کاربر
                db.add(MessageModel(
                    user_id=user.id,
                    role="user",
                    message=user_message
                ))
                await db.commit()

                full_response = ""

                async for token in stream_chat_response(user_message):
                    full_response += token
                    await manager.send_json(session_id, {
                        "type": "stream",
                        "token": token
                    })

                # ذخیره پاسخ AI
                db.add(MessageModel(
                    user_id=user.id,
                    role="assistant",
                    message=full_response
                ))
                await db.commit()

                # history رو sync نگه دار
                history.append(
                    MessageModel(role="user", message=user_message)
                )
                history.append(
                    MessageModel(role="assistant", message=full_response)
                )

    except WebSocketDisconnect:
        pass

    except Exception as e:
        # rollback برای هر خطای غیرمنتظره
        try:
            await db.rollback()
        except Exception:
            pass
        raise e

    finally:
        manager.disconnect(session_id)

































