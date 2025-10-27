from fastapi import FastAPI
from service.authenticaion.api.v1 import routes as auth_v1_route

app = FastAPI()

app.include_router(auth_v1_route.router)
