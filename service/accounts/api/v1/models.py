from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from service.core.database import Base


class AccountModel(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)

    user = relationship("UserModel", back_populates="account")
    
    post = relationship("PostModel", back_populates="account")
