from fastapi import FastAPI 
from users.routes import router as user_router

app = FastAPI(
     title="blog api fastapi")

app.include_router(user_router)