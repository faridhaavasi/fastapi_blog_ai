# celery
from .celery_conf import celery_app

# postapp models
from service.post.api.v1.models import PostModel
from service.user.api.v1.models import UserModel

# AI
from service.AI.AI_func import get_keywords

# database
from service.core.database import SessionLocal, mongo_db


# Celery Tasks
@celery_app.task
def create_new_post(user_id, title, description):
    """
    this function is used to skip the waiting time
     for the user till creating the new post.
    """
    db = SessionLocal()
    try:
        keywords = get_keywords(description)
        new_post = PostModel(
            user_id=user_id,
            title=title,
            description=description,
            tags=keywords
        )
        db.add(new_post)
        db.commit()
        print("===============================")
        print(f"New post created, title: {title}, tags: {keywords}.")
        print("===============================")
    except Exception as e:
        db.rollback()
        print(f"❌ Celery task failed: {e}")
    finally:
        db.close()


@celery_app.task
def update_post(post_id, title, description):
    """
    this function is used to skip the waiting time
     for the user till creating the new post.
    """
    db = SessionLocal()
    try:
        post = db.query(PostModel).filter_by(id=post_id)
        if title:
            post.title = title
        if description:
            post.description = description
            post.tags = get_keywords(description)
        db.commit()
        print("===============================")
        print(f"the post is updated, post_id: {post_id}.")
        print("===============================")
    except Exception as e:
        db.rollback()
        print(f"❌ Celery task failed: {e}")
    finally:
        db.close()
