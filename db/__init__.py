from.engine import Base
from.models import User
from.db.engine import engine
__all__ = ["Base", "User"]

Base.metadata.create_all(bind=engine)