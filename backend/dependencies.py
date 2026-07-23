from dotenv import load_dotenv
import os
from pwdlib import PasswordHash
import jwt
from fastapi import HTTPException
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta, UTC


Secret_key = os.environ["SECRET_KEY"]

pass_hash = PasswordHash.recommended()
algorithm = "HS256"
token_expire_time = 30


def verify_password(plain_pass: str, hashed_pass: str):
    return pass_hash.verify(plain_pass, hashed_pass)


def get_pass_hash(password: str):
    return pass_hash.hash(password)

# This function Is to be used to generate a JWT token when Logging in or Creating an acc Or refreshing the token


def generate_token(payload: dict, expires_delta: timedelta = None):
    to_encode = payload.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=token_expire_time)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Secret_key, algorithm=algorithm)
    return encoded_jwt


# This function reads the token and returns the payload and checks the expiry


def decode_token(token: str):
    try:
        data = jwt.decode_complete(
            token, key=Secret_key, algorithms=[algorithm])
        payload = data["payload"]
        header = data["header"]
        if header.get("alg") != algorithm:
            raise HTTPException(
                status_code=401, detail="Forbidden: Invalid Token")
        id = payload["sub"]

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="Forbidden: Token Has Expired")
    except InvalidTokenError:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid Token")
    return id
