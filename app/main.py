import socket, uvicorn
from datetime import datetime, timedelta
from typing import Union

from fastapi import FastAPI, Body, Header
from fastapi.middleware.cors import CORSMiddleware
import random, time
from scriptmgr import ScriptManager
scriptMgr = ScriptManager()

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

def createBook(no: int):
    return { 'id': f'book-{no}', 'title': f'Book {no}', 'author_id': 'peter_pan', 'author_name': 'Peter Pan'}
def createAirplanTicket(no: int):
    td = random.randint(0, 30)
    departureTime = datetime.now() + timedelta(days=td)
    arrivalTime = departureTime + timedelta(days=random.randint(1,2))
    return { 'id': 'ticket01', 'departure_time': departureTime.isoformat(), 'arrival_time': arrivalTime.isoformat(), 'departure_place': 'hcm', 'arrival_place': 'hanoi'}

@app.get("/object/{category}")
def generate_object_info_by_category(category):
    if category == 'book':
        return createBook(1)
    if category == 'ticket':
        return createAirplanTicket(1)
    return {"id": 'sample-object-01', "name": 'This is object Name' }

@app.get("/objects/{category}/{pageSize}")
def generate_objects_info_by_category(category, pageSize:int, delaySeconds: int = Header(default=0)):
    ls = []
    for i in range(pageSize):
        rnd = random.randint(1, 100)
        if category == 'book':
            ls += [createBook(i)]
        else:
            ls += [createAirplanTicket(i)]

    if delaySeconds > 0:
        print(f'Sleep for {delaySeconds} seconds...')
        time.sleep(delaySeconds)
    return ls


@app.post("/auth/basic/login")
def basicSignInJWT(account_id:str=Body(), password:str=Body()):
    return auth.basicSignInJWT(tokenService, account_id, password)
    
@app.get("/user/me")
def getUserInfo(token:str=Header()):
    return auth.getUserInfo(tokenService, token)
    
# @app.post("/mock/api/login")
# def mockLogin(body: dict = Body()):
#     script = scriptMgr.loadScript('mockLogin')
#     if script == None:
#         print('Script not found => return body')
#         return body
    
#     response = body
#     exec(script, {'body': body})
#     return response

@app.post("/mock/api/{token1}")
def mockPostBodyOne(token1:str, body: dict = Body()):
    script = scriptMgr.loadScript(f'postBody_{token1}')
    if script == None:
        print('Script not found => return body')
        return body
    
    global response
    response = 'no data'
    exec(script, {'body': body}, {'tokens': [token1]})
    return response

@app.get("/mock/api/{token1}")
def mockGetOne(token1:str):
    script = scriptMgr.loadScript(f'get_{token1}')
    if script == None:
        print('Script not found => return body')
        return f'script not found: get_{token1}'
    
    global response
    response = 'no data'
    exec(script, globals(), {'tokens': [token1]})
    return response

@app.post("/mock/api/{token1}/{token2}")
def mockPostBodyTwo(token1:str, token2:str, body: dict = Body()):
    script = scriptMgr.loadScript(f'postBody_{token1}_{token2}')
    if script == None:
        print('Script not found => return body')
        return body
    
    global response
    response = 'no data'
    exec(script, {'body': body, 'tokens': [token1, token2]})
    return response

@app.get("/mock/api/{token1}/{token2}")
def mockGetTwo(token1:str, token2:str):
    script = scriptMgr.loadScript(f'get_{token1}_{token2}')
    if script == None:
        print('Script not found => return body')
        return 'script not found'
    
    global response
    response = 'no data'
    exec(script, {'tokens': [token1, token2]})
    return response

@app.post("/mock/api/{token1}/{token2}/{token3}")
def mockPostBodyThree(token1:str, token2:str, token3:str, body: dict = Body()):
    script = scriptMgr.loadScript(f'postBody_{token1}_{token2}_{token3}')
    if script == None:
        print('Script not found => return body')
        return body
    
    global response
    response = 'no data'
    exec(script, {'body': body, 'tokens': [token1, token2, token3]})
    return response

@app.get("/mock/api/{token1}/{token2}/{token3}")
def mockGetThree(token1:str, token2:str, token3:str):
    script = scriptMgr.loadScript(f'get_{token1}_{token2}_{token3}')
    if script == None:
        print('Script not found => return body')
        return 'script not found'
    
    global response
    response = 'no data'
    exec(script, {'tokens': [token1, token2, token3]})
    return response

@app.post("/script/{key}")
def saveScript(key:str, script:str = Body(media_type='text/plain')):
    scriptMgr.saveScript(key, script)
    return script

@app.get("/script/{key}")
def loadScriptOfApi(key:str):
    script = scriptMgr.loadScript(key)    
    if script == None:
        return ''
    return {'script': script}

@app.get("/scripts")
def loadAllScripts():
    return scriptMgr.getScriptList()    
    

def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP


if __name__ == '__main__':
    uvicorn.run("main:app", host=extract_ip(), port=24502)