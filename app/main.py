from datetime import datetime, timedelta
from typing import Union

from fastapi import FastAPI, Body, Header
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = '*',
    allow_credentials=True,
    allow_methods = '*',
    allow_headers = '*'
)

import auth
from token_service import TokenService

tokenService = TokenService()

@app.get("/")
def welcome():
    return 'welcome'


@app.get("/object/{category}")
def generate_object_info_by_category(category):
    if category == 'book':
        return { 'id': 'book01', 'title': 'Book 1', 'author_id': 'peter_pan', 'author_name': 'Peter Pan'}
    return {"id": 'sample-object-01', "name": 'This is object Name' }


@app.post("/auth/basic/login")
def basicSignInJWT(account_id:str=Body(), password:str=Body()):
    return auth.basicSignInJWT(tokenService, account_id, password)
    
@app.get("/user/me")
def getUserInfo(token:str=Header()):
    return auth.getUserInfo(tokenService, token)
    
