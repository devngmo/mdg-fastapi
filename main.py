from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def welcome():
    return 'welcome'


@app.get("/object/{category}")
def generate_object_info_by_category(category):
    if category == 'book':
        return { 'id': 'book01', 'title': 'Book 1', 'author_id': 'peter_pan', 'author_name': 'Peter Pan'}
    return {"id": 'sample-object-01', "name": 'This is object Name' }