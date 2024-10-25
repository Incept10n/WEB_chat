from datetime import datetime, timedelta, timezone
import hashlib

from fastapi import HTTPException
import jwt

from service.Constants import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

import requests


def hash_sha256(data: str) -> str:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data.encode('utf-8'))
    return sha256_hash.hexdigest()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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