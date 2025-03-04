from fastapi import FastAPI
from random import randint
app = FastAPI()

names = [
    {'id': 1, 'name':'farid'},
    {'id': 2, 'name':'ali'},
]

@app.get('/')
def index():
    return {'message': 'hello word'}

@app.get('/names')
def show_all_name():
    return names

@app.get('/names/{id}')
def dtail_name(id: int):
    for name in names:
        if name['id']==id:
            return name
        return {"error": "Name not found"}
    
@app.post('/names')
def create_name(name:str):
    id = randint(3,100)
    names.append({'id': id, 'name': name})
    return names