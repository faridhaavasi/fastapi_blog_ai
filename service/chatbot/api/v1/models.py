# Sqlalchemy
from sqlalchemy import(
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship

# Database
from service.core.database import Base


class MessageModel(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    role = Column(String, default='AI', nullable=False)

    message = Column(String, nullable=False)

    created_date = Column(DateTime, server_default=func.now())

    user = relationship("UserModel", uselist=False)