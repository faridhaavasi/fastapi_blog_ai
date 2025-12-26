# Python
from urllib.parse import unquote

# FastAPI
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException

# SQLALCHEMY
from sqlalchemy import select

# Database (postgresql)
from service.core.database import AsyncSessionLocal

# chatbot app models
from .models import MessageModel

# post app models
from service.post.api.v1.models import PostModel

# JWT
from service.auth.jwt_auth import get_user_via_access_token_async

# AI
from service.AI.AI_func import stream_chat_response, stream_chat_response_post

# chatbot app router
router = APIRouter(prefix="/chatbot/api/v1", tags=["chatbot_api_v1"])

# Chat Bot
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

            result = await db.execute(
                select(MessageModel)
                .where(MessageModel.user_id == user.id)
                .order_by(MessageModel.created_date)
            )

            messages = result.scalars().all()

            for msg in messages:
                await websocket.send_text(f"{msg.role}: {msg.message}")

            while True:
                user_message = await websocket.receive_text()

                new_user_message = MessageModel(user_id=user.id, role='user', message=user_message)

                db.add(new_user_message)
                await db.commit()

                ai_chunks = []

                async for chunk in stream_chat_response(user_message):
                    ai_chunks.append(chunk)
                    await websocket.send_text(chunk)

                ai_message = "".join(ai_chunks)

                prefixes = [
                    f"you: {user_message}",
                    f"user: {user_message}",
                    user_message
                ]
                for p in prefixes:
                    if ai_message.lower().startswith(p.lower()):
                        ai_message = ai_message[len(p):].lstrip()

                ai_msg = MessageModel(
                    user_id=user.id,
                    role="ai",
                    message=ai_message
                )
                db.add(ai_msg)
                await db.commit()
    except WebSocketDisconnect:
        print("Client disconnected")
    except HTTPException:
        await websocket.close(code=1008)


# Post Chat Bot
@router.websocket("/post_ws/{jwt_access_token}")
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

            result = await db.execute(
                select(PostModel)
                .where(PostModel.user_id == user.id)
                .order_by(PostModel.created_date.desc())
                .limit(5)
            )

            last_posts = [row[0] for row in result.all()]

            messages = result.scalars().all()

            for msg in messages:
                await websocket.send_text(f"{msg.role}: {msg.message}")

            while True:
                user_message = await websocket.receive_text()

                new_user_message = MessageModel(user_id=user.id, role='user', message=user_message)

                db.add(new_user_message)
                await db.commit()

                ai_chunks = []

                async for chunk in stream_chat_response_post(user_message, last_posts):
                    ai_chunks.append(chunk)
                    await websocket.send_text(chunk)

                ai_message = "".join(ai_chunks)

                prefixes = [
                    f"you: {user_message}",
                    f"user: {user_message}",
                    user_message
                ]
                for p in prefixes:
                    if ai_message.lower().startswith(p.lower()):
                        ai_message = ai_message[len(p):].lstrip()

                ai_msg = MessageModel(
                    user_id=user.id,
                    role="ai",
                    message=ai_message
                )
                db.add(ai_msg)
                await db.commit()
    except WebSocketDisconnect:
        print("Client disconnected")
    except HTTPException:
        await websocket.close(code=1008)