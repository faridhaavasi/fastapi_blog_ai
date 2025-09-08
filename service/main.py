from fastapi import FastAPI 
from users.routes import router as user_routes

app = FastAPI(
     title="Blog Application",
    description=(
        "A simple and efficient blog advance API built with FastAPI. "
        "This API allows users to create, retrieve, update, and delete post. "
        "It is designed for task tracking and productivity improvement."
    ),
    version="1.0.0",
)

app.include_router(user_routes)



