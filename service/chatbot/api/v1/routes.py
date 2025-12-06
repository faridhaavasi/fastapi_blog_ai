# FastAPI
from fastapi import APIRouter, status, Cookie, Depends, HTTPException
from typing import List

# SQLALCHEMY
from sqlalchemy.orm import Session

# Database (postgresql)
from service.core.database import get_db

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


# chatbot app router
router = APIRouter(prefix="/chatbot/api/v1", tags=["chatbot_api_v1"])


@router.post('/get_all_messages', status_code=status.HTTP_200_OK, response_model=List[GetAllMassageSchema])
async def user_create_post(jwt_access_token: str = Cookie(None), db: Session=Depends(get_db)):
    user = get_user_via_access_token(jwt_access_token)
    if user:
        all_messages = db.query(MessageModel).filter_by(user_id=user.id).all()
        if all_messages:
            return all_messages
        raise HTTPException(detail='no messages yet',
                            status_code=status.HTTP_404_NOT_FOUND)
    raise HTTPException(detail='we couldn\'t verify you with provided credentials.',
                        status_code=status.HTTP_401_UNAUTHORIZED)




























