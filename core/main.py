from fastapi import FastAPI
from random import randint

app = FastAPI()

names = [
    {'id': 1, 'name': 'farid'},
    {'id': 2, 'name': 'ali'},
]

@app.get('/')
def index():
    return {'message': 'hello world'}

@app.get('/names')
def show_all_name():
    return names

@app.get('/names/{id}')
def detail_name(id: int):
    for name in names:
        if name['id'] == id:
            return name
    return {"error": "Name not found"}  
@app.post('/names')
def create_name(name: str):
    id = randint(3, 100)
    names.append({'id': id, 'name': name})
    return names

@app.put('/names/{id}')
def update_name(id: int, name: str):
    for item in names:
        if item['id'] == id:
            item['name'] = name  
            return {'message': 'Updated successfully'}
    return {'message': 'Name not found'} 

@app.delete('/names/{id}')
def delelte_name(id: int):
    for index, item in enumerate(names):
        if item['id'] == id:
            del names[index]  
            return {'message': 'Deleted successfully'}
    
    return {'message': 'Name not found'}   


