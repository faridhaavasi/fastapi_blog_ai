from sqlalchemy.orm import Mapped, mapped_column
from. engine import Base
class User(Base):
    __tablename__ = "users"

    id: [int] = mapped_column( primary_key=True, autoincrement=True, unique=True, index=True) 
    username: [str] = mapped_column( default=None, unique=True)
    email: [str] = mapped_column(default=[str | None] , unique=True)
    password : [str] = mapped_column()
