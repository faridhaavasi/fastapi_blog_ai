# Sqlalchemy
from sqlalchemy import(
    Column,
    String,
    Integer,
    JSON,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship

# Database
from service.core.database import Base


# posts model
class PostModel(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    title = Column(String, nullable=False)

    description = Column(String, nullable=False)

    tags = Column(JSON)

    created_date = Column(DateTime, server_default=func.now())

    updated_date = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now()
    )

    user = relationship("UserModel", uselist=False)


# likes model
class LikeModel(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    post_id = Column(Integer, ForeignKey("posts.id"))

    created_date = Column(DateTime, server_default=func.now())

    user = relationship("UserModel", uselist=False)

    post = relationship("PostModel", uselist=False)


# comments model
class CommentModel(Base):
    __tablename__  = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    post_id = Column(Integer, ForeignKey("posts.id"))

    comment = Column(String, nullable=False)

    created_date = Column(DateTime, server_default=func.now())

    updated_date = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now()
    )

    user = relationship("UserModel", uselist=False)

    post = relationship("PostModel", uselist=False)
































