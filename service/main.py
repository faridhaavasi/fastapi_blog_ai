from fastapi import FastAPI 


app = FastAPI(
     title="blog api fastapi")

@app.get('/')
async def index():
    return {}