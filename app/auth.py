from datetime import datetime, timedelta
import jwt
from token_service import TokenService

JWT_SECRET_KEY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def createJWTToken(metadata:dict, expires_delta: timedelta):
        to_encode = metadata.copy()
        expire = datetime.now() + expires_delta
        
        print('JWT create token expire: ', expire.isoformat())
        to_encode.update({'exp': expire})
        tokenBytes = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm='HS256')
        token = tokenBytes.decode()
        return token

def basicSignInJWT(tokenService: TokenService, accountID:str, password:str):
    expireTime = datetime.now() + timedelta(minutes=15)
    dateDiff = expireTime-datetime.now()

    roles = []
    if accountID == 'admin':
        roles = ['admin']
    else:
        roles = ['user']
    loginSession = { 'account_id':accountID, 'roles': roles, 'account_name': accountID }

    token = createJWTToken(loginSession, dateDiff )
    tokenService.set(token, loginSession)

    return { 'account_id': accountID, 'account_name': accountID, 'access_token': token, 'ttl': dateDiff.seconds, 'expire': expireTime.isoformat() }

def getUserInfo(tokenService: TokenService, token):
    return tokenService.get(token)