from fastapi import FastAPI

app = FastAPI()

@app.get('/home/{name}')
def index(name: str, age :int=0):
    return {'message': f" hi  {name} {age} yers old"}