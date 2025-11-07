from fastapi import FastAPI
from service.authenticaion.api.v1 import routes as auth_v1_route
from service.post.api.v1 import routes as post_v1_route

app = FastAPI()

app.include_router(auth_v1_route.router)
app.include_router(post_v1_route.router)
