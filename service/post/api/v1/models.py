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


# PostModel
   
class PostModel(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String, nullable=False)

    description = Column(String, nullable=False)

    tags = Column(JSON)

    created_date = Column(DateTime, server_default=func.now())

    updated_date = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    # Relationships
    user = relationship("UserModel", back_populates="posts")

    likes = relationship("LikeModel", back_populates="post", cascade="all, delete")

    comments = relationship("CommentModel", back_populates="post", cascade="all, delete")

    account = relationship("AccountModel", back_populates="post", uselist=False)

# likes model
class LikeModel(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)

    created_date = Column(DateTime, server_default=func.now())

    user = relationship("UserModel", back_populates="likes")

    post = relationship("PostModel", back_populates="likes")
# comments model

class CommentModel(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)

    comment = Column(String, nullable=False)

    created_date = Column(DateTime, server_default=func.now())

    updated_date = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    user = relationship("UserModel", back_populates="comments")
    
    post = relationship("PostModel", back_populates="comments")
































