# FastAPI
from fastapi import APIRouter, status, Depends, HTTPException, Cookie
from typing import List

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
    GetAllPostCommentsSchema,
)

# post app models
from .models import PostModel, LikeModel, CommentModel

# celery tasks
from service.celery_config.celery_task import create_new_post, update_user_post

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
        all_posts = db.query(PostModel).all()
        user_liked_tags = mongo_db.liked_tags.find_one({'id': user.id}, {'_id': 0})['tags']
        recommended_post_list_id = []
        recommended_count = 0
        for post in all_posts:
            tags_in_common = len(set(post.tags) & set(user_liked_tags))
            if tags_in_common > 0 and recommended_count < 2:
                recommended_post_list_id.append(post.id)
                recommended_count += 1
            elif tags_in_common == 0 and recommended_count >= 1:
                recommended_post_list_id.append(post.id)
                recommended_count = 0
        return [post for post in all_posts if post.id in recommended_post_list_id]
    raise HTTPException(detail='we couldn\'t verify you with provided credentials.',
                        status_code=status.HTTP_401_UNAUTHORIZED)


@router.get('/get_post/{post_id}/', status_code=status.HTTP_200_OK, response_model=GetAllPostSchema)
async def get_post_via_id(post_id: int, jwt_access_token: str = Cookie(None), db: Session = Depends(get_db)):
    user = get_user_via_access_token(jwt_access_token, db)
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
    user = get_user_via_access_token(jwt_access_token, db)
    if user:
        post = db.query(PostModel).filter_by(id=post_id).one_or_none()
        if post:
            if post.user_id == user.id:
                update_user_post.delay(post.id, request.title, request.description)
                return {'detail': 'your changes will be published soon.'}
            raise HTTPException(detail='this post is not yours.',
                                status_code=status.HTTP_403_FORBIDDEN)
        raise HTTPException(detail='we couldn\'t find the post',
                            status_code=status.HTTP_404_NOT_FOUND)
    raise HTTPException(detail='we couldn\'t verify you with provided credentials.',
                        status_code=status.HTTP_401_UNAUTHORIZED)


@router.delete('/delete_post/{post_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, jwt_access_token: str = Cookie(None), db: Session = Depends(get_db)):
    user = get_user_via_access_token(jwt_access_token, db)
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
async def create_delete_like(post_id: int, jwt_access_token: str = Cookie(None), db: Session = Depends(get_db)):
    user = get_user_via_access_token(jwt_access_token, db)
    if user:
        post = db.query(PostModel).filter_by(id=post_id).one_or_none()
        if post:
            like_relation = db.query(LikeModel).filter_by(user_id=user.id, post_id=post.id).one_or_none()
            if not like_relation:
                new_like_relation = LikeModel(user_id=user.id, post_id=post.id)
                db.add(new_like_relation)
                db.commit()
                user_liked_tags = mongo_db.liked_tags.find_one({'id':user.id},{'_id':0})['tags']
                updated_tags = list(set(user_liked_tags + post.tags))
                mongo_db.liked_tags.update_one({'id':user.id},{'$set':{'tags': updated_tags}})
                return {'detail': 'the liked this post.'}
            db.delete(like_relation)
            db.commit()
            return HTTPException(detail='your like relation is removed.',
                        status_code=status.HTTP_204_NO_CONTENT)
        raise HTTPException(detail='we couldn\'t find the post',
                            status_code=status.HTTP_404_NOT_FOUND)
    raise HTTPException(detail='we couldn\'t verify you with provided credentials.',
                        status_code=status.HTTP_401_UNAUTHORIZED)


@router.post('/comment_post/{post_id}/', status_code=status.HTTP_201_CREATED)
async def create_comment(request: UserCreateCommentSchema, post_id: int, jwt_access_token: str = Cookie(None), db: Session = Depends(get_db)):
    user = get_user_via_access_token(jwt_access_token, db)
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


@router.get('/get_post_comment/{post_id}/', status_code=status.HTTP_200_OK, response_model=List[GetAllPostCommentsSchema])
async def get_post_comment(post_id: int, jwt_access_token: str = Cookie(None), db: Session = Depends(get_db)):
    user = get_user_via_access_token(jwt_access_token, db)
    if user:
        post = db.query(PostModel).filter_by(id=post_id).one_or_none()
        if post:
            comments = db.query(CommentModel).filter_by(post_id=post_id).all()
            return comments
        raise HTTPException(detail='we couldn\'t find the post',
                            status_code=status.HTTP_404_NOT_FOUND)
    raise HTTPException(detail='we couldn\'t verify you with provided credentials.',
                        status_code=status.HTTP_401_UNAUTHORIZED)
















