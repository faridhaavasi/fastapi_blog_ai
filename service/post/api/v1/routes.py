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
    UserUpdatePostSchema,
    UserCreateCommentSchema,
    GetAllPostSchema,
)

# post app models
from .models import PostModel, LikeModel, CommentModel

# user app models
from service.user.api.v1.models import UserModel

# celery tasks
from service.celery_config.celery_task import create_new_post, update_post

# JWT
from service.auth.jwt_auth import get_user_via_access_token

# post app router
router = APIRouter(prefix="/post/api/v1", tags=["post_api_v1"])

# mongo_db.liked_tags.find({},{'_id':0}).to_list()

# mongo_db.liked_tags.insert_one(
#         {
#             'id':user.id,
#             'tags':['AI','python','cars'],
#         }
#     )


@router.post('/create_post', status_code=status.HTTP_201_CREATED)
async def user_create_post(request: UserCreatePostSchema, jwt_access_token: str = Cookie(None),
                           db: Session=Depends(get_db)):
    user = get_user_via_access_token(jwt_access_token, db)
    if user:
        create_new_post.delay(user.id, request.title, request.description)
        return {'detail': 'your new post will be created soon.'}
    raise HTTPException(detail='we couldn\'t verify you with provided credentials.',
                        status_code=status.HTTP_401_UNAUTHORIZED)


@router.get('/get_posts', status_code=status.HTTP_200_OK, response_model=List[GetAllPostSchema])
async def get_all_posts( jwt_access_token: str = Cookie(None), db: Session=Depends(get_db)):
    user = get_user_via_access_token(jwt_access_token, db)
    if user:
        return db.query(PostModel).all()
    raise HTTPException(detail='we couldn\'t verify you with provided credentials.')


@router.get('/get_post/{post_id}/', status_code=status.HTTP_200_OK)
async def get_post_via_id(post_id: int, jwt_access_token: str = Cookie(None), db: Session = Depends(get_db)):
    user = get_user_via_access_token(jwt_access_token)
    if user:
        post = db.query(PostModel).filter_by(id=post_id).one_or_none()
        if post:
            return post
        raise HTTPException(detail='we couldn\'t find the post.',
                            status_code=status.HTTP_404_NOT_FOUND)
    raise HTTPException(detail='we couldn\'t verify you with provided credentials.',
                            status_code=status.HTTP_401_UNAUTHORIZED)


@router.put('/update_post/{post_id}/', status_code=status.HTTP_201_CREATED)
async def update_post(request: UserUpdatePostSchema, post_id: int, jwt_access_token: str = Cookie(None),
                      db: Session = Depends(get_db)):
    user = get_user_via_access_token(jwt_access_token)
    if user:
        post = db.query(PostModel).filter_by(id=post_id).one_or_none()
        if post:
            if post.user_id == user.id:
                update_post.delay(post.id, request.title, request.description)
                return {'detail': 'your changes will be published soon.'}
            raise HTTPException(detail='this post is not yours.',
                                status_code=status.HTTP_403_FORBIDDEN)
        raise HTTPException(detail='we couldn\'t find the post',
                            status_code=status.HTTP_404_NOT_FOUND)
    raise HTTPException(detail='we couldn\'t verify you with provided credentials.',
                        status_code=status.HTTP_401_UNAUTHORIZED)


@router.delete('/delete_post/{post_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def get_mongo_object(post_id: int, jwt_access_token: str = Cookie(None), db: Session = Depends(get_db)):
    user = get_user_via_access_token(jwt_access_token)
    if user:
        post = db.query(PostModel).filter_by(id=post_id).one_or_none()
        if post:
            if post.user_id == user.id:
                db.delete(post)
                db.commit()
                return {'detail': 'the post is deleted.'}
            raise HTTPException(detail='this post is not yours.',
                                status_code=status.HTTP_403_FORBIDDEN)
        raise HTTPException(detail='we couldn\'t find the post',
                            status_code=status.HTTP_404_NOT_FOUND)
    raise HTTPException(detail='we couldn\'t verify you with provided credentials.',
                        status_code=status.HTTP_401_UNAUTHORIZED)


@router.get('/like_post/{post_id}/', status_code=status.HTTP_200_OK)
async def get_mongo_object(post_id: int, jwt_access_token: str = Cookie(None), db: Session = Depends(get_db)):
    pass


@router.post('/comment_post/{post_id}/', status_code=status.HTTP_201_CREATED)
async def get_mongo_object(request: UserCreateCommentSchema, post_id: int, jwt_access_token: str = Cookie(None), db: Session = Depends(get_db)):
    user = get_user_via_access_token(jwt_access_token)
    if user:
        post = db.query(PostModel).filter_by(id=post_id).one_or_none()
        if post:
            new_comment = CommentModel(user_id=user.id, post_id=post.id, comment=request.comment)
            db.add(new_comment)
            db.commit()
            return {'detail': f'you commented on post {post.id}.'}
        raise HTTPException(detail='we couldn\'t find the post',
                            status_code=status.HTTP_404_NOT_FOUND)
    raise HTTPException(detail='we couldn\'t verify you with provided credentials.',
                        status_code=status.HTTP_401_UNAUTHORIZED)
















