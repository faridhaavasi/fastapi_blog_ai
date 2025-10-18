from fastapi import FastAPI
from authenticaion import routes as auth_route

app = FastAPI()

app.include_router(auth_route.router)   
