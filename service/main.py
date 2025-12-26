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

@app.get("/chatbot/{jwt_access_token}", response_class=HTMLResponse)
async def chatbot_demo(jwt_access_token: str):
    # فایل HTML را باز می‌کنیم
    with open("static/chatbot.html") as f:
        html_content = f.read()
    # مقدار JWT جایگزین template می‌شود
    html_content = html_content.replace("{{JWT_TOKEN}}", jwt_access_token)
    return HTMLResponse(content=html_content)

@app.get("/post_chatbot/{jwt_access_token}", response_class=HTMLResponse)
async def chatbot_demo(jwt_access_token: str):
    # فایل HTML را باز می‌کنیم
    with open("static/post_chatbot.html") as f:
        html_content = f.read()
    # مقدار JWT جایگزین template می‌شود
    html_content = html_content.replace("{{JWT_TOKEN}}", jwt_access_token)
    return HTMLResponse(content=html_content)
