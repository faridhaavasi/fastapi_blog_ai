from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from service.authenticaion.api.v1 import routes as auth_v1_route
from service.post.api.v1 import routes as post_v1_route
from service.chatbot.api.v1 import routes as chatbot_v1_route

app = FastAPI()

app.include_router(auth_v1_route.router)
app.include_router(post_v1_route.router)
app.include_router(chatbot_v1_route.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/chatbot_demo", response_class=HTMLResponse)
async def chatbot_demo():
    with open("static/chatbot.html") as f:
        return f.read()