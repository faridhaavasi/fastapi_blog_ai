# Python
import os
from dotenv import load_dotenv

# Sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Mongodb
from pymongo import MongoClient

# config
from .config import settings

load_dotenv()

"""
    POSTGRESQL_DB
"""
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,

)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
    MONGO_DB
"""
# getting the Mongodb url from .env
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:mongo@mongodb:27017/mydb?authSource=admin")

# creating mongodb client
client = MongoClient(MONGO_URL)

# setting the db to the database you set in your MONGO_URL in .env file
mongo_db = client.get_database()

