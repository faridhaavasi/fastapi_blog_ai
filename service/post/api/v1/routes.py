# FastAPI
from fastapi import APIRouter, status, Depends, HTTPException

# Database
from service.core.database import get_db

# SQLALCHEMY
from sqlalchemy.orm import Session

# post app schemas
from .schemas import (
    UserCreatePostSchema,
)

# post app models
from .models import PostModel, LikeModel, CommentModel

# AI funcs
from service.AI.AI_func import get_keywords


# post app router
router = APIRouter(prefix="/post/api/v1", tags=["post_api_v1"])


@router.post('/create_post', status_code=status.HTTP_201_CREATED)
async def user_create_post(request: UserCreatePostSchema, db: Session = Depends(get_db)):
    return {'detail': 'we are online...'}