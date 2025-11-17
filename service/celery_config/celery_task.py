import logging
from .celery_conf import celery_app
from service.post.api.v1.models import PostModel
from service.user.api.v1.models import UserModel
from service.AI.AI_func import get_keywords
from service.core.database import SessionLocal


logger = logging.getLogger(__name__)


def db_session():
    """Session manager for Celery (context manager)."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.exception("Database error: %s", e)
        raise
    finally:
        db.close()


@celery_app.task
def create_new_post(user_id: int, title: str, description: str) -> None:
    with db_session() as db:
        keywords = get_keywords(description)

        new_post = PostModel(
            user_id=user_id,
            title=title,
            description=description,
            tags=keywords
        )
        db.add(new_post)

        logger.info(f"New post created (title={title}, tags={keywords})")


@celery_app.task
def update_user_post(post_id: int, title: str, description: str) -> None:
    with db_session() as db:
        post = db.query(PostModel).filter_by(id=post_id).one_or_none()

        if not post:
            logger.error(f"Post not found: {post_id}")
            return

        if title:
            post.title = title

        if description:
            post.description = description
            post.tags = get_keywords(description)

        logger.info(f"Post updated (post_id={post_id})")
