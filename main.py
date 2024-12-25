from fastapi import FastAPI , Body
from pydantic import BaseModel

class Postcreate(BaseModel):
    title: str
    content: str

app = FastAPI()

@app.get('/post/{slug}')
async def get_post(slug: str):
    return {"slug": slug}


@app.post('/post/create')
async def create_post(post: Postcreate = Body()):
    return post

