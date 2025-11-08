# FastAPI
from fastapi import APIRouter, status, Depends, HTTPException, Cookie
from typing import List

# JWT
from service.auth.jwt_auth import get_authenticated_user

# Database (postgresql)
from service.core.database import get_db

# Database (mongodb)
from service.core.database import mongo_db

# SQLALCHEMY
from sqlalchemy.orm import Session

# post app schemas
from .schemas import (
    UserCreatePostSchema,
    GetAllPostSchema,
)

# post app models
from .models import PostModel, LikeModel, CommentModel

# user app models
from service.user.api.v1.models import UserModel

# celery tasks
from service.celery_config.celery_task import create_new_post

# JWT
from service.auth.jwt_auth import get_user_via_access_token

# post app router
router = APIRouter(prefix="/post/api/v1", tags=["post_api_v1"])


@router.post('/create_post', status_code=status.HTTP_201_CREATED)
async def user_create_post(request: UserCreatePostSchema, jwt_access_token: str = Cookie(None),
                           db: Session=Depends(get_db)):
    user = get_user_via_access_token(jwt_access_token, db)
    if user:
        create_new_post.delay(user.id, request.title, request.description)
        return {'detail': 'your new post will be created soon.'}
    raise HTTPException(detail='we couldn\'t verify you with provided credentials.',
                        status_code=status.HTTP_401_UNAUTHORIZED)


@router.get('/create_mongo_object', status_code=status.HTTP_201_CREATED)
async def create_mongo_object(jwt_access_token: str = Cookie(None), db: Session=Depends(get_db)):
    user = get_user_via_access_token(jwt_access_token, db)
    mongo_db.liked_tags.insert_one(
        {
            'id':user.id,
            'tags':['AI','python','cars'],
        }
    )
    return {'detail': 'new mongo object was created'}


@router.get('/get_posts', status_code=status.HTTP_200_OK, response_model=List[GetAllPostSchema])
async def get_all_posts( jwt_access_token: str = Cookie(None), db: Session=Depends(get_db)):
    user = get_user_via_access_token(jwt_access_token, db)
    if user:
        return db.query(PostModel).all()
    raise HTTPException(detail='we couldn\'t verify you with provided credentials.')


@router.get('/get_mongo_object', status_code=status.HTTP_200_OK)
async def get_mongo_object( jwt_access_token: str = Cookie(None), db: Session = Depends(get_db)):
    user = get_user_via_access_token(jwt_access_token, db)
    if user:
        return mongo_db.liked_tags.find({},{'_id':0}).to_list()
    raise HTTPException(detail='we couldn\'t verify you with provided credentials.')


















