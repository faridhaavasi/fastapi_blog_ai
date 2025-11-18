from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    func,
    Integer,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from service.core.database import Base

from passlib.context import CryptContext

from post.api.v1.models import PostModel

from accounts.api.v1.models import AccountModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserModel(Base):
    __tablename__ = "users"
    
     
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=True)
    is_active = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    created_date = Column(DateTime, server_default=func.now())
    updated_date = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    # Relationships
    posts = relationship("PostModel", back_populates="user", cascade="all, delete")
    likes = relationship("LikeModel", back_populates="user", cascade="all, delete")
    comments = relationship("CommentModel", back_populates="user", cascade="all, delete")
    account = relationship("AccountModel", back_populates="user", uselist=False)

    def hash_password(self, plain_password: str) -> str:
        return pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)

    def set_password(self, plain_text: str) -> None:
        self.password = self.hash_password(plain_text)


class TokenModel(Base):
    __tablename__ = "tokens"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    
    token = Column(String, nullable=False, unique=True)
    
    created_date = Column(DateTime, server_default=func.now())
    
    user = relationship("UserModel", uselist=False)
    

