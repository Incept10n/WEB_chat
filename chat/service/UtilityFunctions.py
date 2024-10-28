from fastapi import HTTPException
import jwt

from service.Constants import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

import requests

def is_token_valid(access_token):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Token is invalid")

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=403, detail="Token does not contain user_id")

    user_email = payload.get("email")
    if user_email is None:
        raise HTTPException(status_code=403, detail="Token does not contain email")

    return user_id, user_email

def is_chat_exist(chatName: str):
    response = requests.get(f'http://nginx/is_chat_exist?name={chatName}')
    if (response.status_code != 200):
        raise HTTPException(status_code=404, detail="The chat does not exist")
    return response.json()