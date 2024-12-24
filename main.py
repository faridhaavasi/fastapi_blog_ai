from fastapi import FastAPI
from pydantic import BaseModel

class Person(BaseModel):
    name : str
    age: int
    hirgt: int | None = None

app = FastAPI()

@app.get('/home/{name}')
def index(name: str, age :int=0):
    return {'message': f" hi  {name} {age} yers old"}

@app.post('/post_page')
def post_page(person_data: Person):
    return person_data        