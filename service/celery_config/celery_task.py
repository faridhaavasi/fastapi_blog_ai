# celery
from .celery_conf import celery_app

# database
from service.core.database import get_db

# postapp models
from service.post.api.v1.models import PostModel

# AI
from service.AI.AI_func import get_keywords

# database
from service.core.database import Session, mongo_db


@celery_app.task
def create_new_post(user, title, description):
    db = Session()
    keywords = get_keywords(description)
    new_post = PostModel(user_id=user.id, title=title, description=description, tags=keywords)
    db.add(new_post)
    db.commit()
    print("===============================")
    print(f"new post was created, title: {title} and tags: {keywords}.")
    print("===============================")
    db.close()
