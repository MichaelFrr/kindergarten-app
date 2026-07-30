"""This Module Hosts Dependencies Used In Other Folders Such As Jwt, PassHashing"""
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, UTC
from typing import Annotated
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from backend.database import getdb, Select, Session
from backend.models import User, Child, Classroom
from backend.redis_client import r
import secrets

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
load_dotenv()

Secret_key = os.environ["SECRET_KEY"]



pass_hash = PasswordHash.recommended()

ALGORITHM = "HS256"
TOKEN_EXPIRE_TIME = 1     # this one is in minutes
REFRESH_TOKEN_EXPIRE_DAYS = 30    # this one is in days


def generate_opaque_token():
    return secrets.token_urlsafe(32)


def get_refresh(uuid):
    return r.get(f"refresh:{uuid}")

def set_refresh_token(uuid):
    expire_seconds = int(timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS).total_seconds())
    refresh_token = generate_opaque_token()
    r.setex(f"refresh:{uuid}", expire_seconds, refresh_token )
    return refresh_token

def get_blacklisted(access_token):
    return r.get(f"blacklist:{access_token}")

def blacklist_token(access_token, access_token_expire_seconds):
    r.setex(f"blacklist:{access_token}", access_token_expire_seconds, "blacklisted")


def verify_password(plain_pass: str, hashed_pass: str):

    return pass_hash.verify(plain_pass, hashed_pass)


def get_pass_hash(password: str):
    return pass_hash.hash(password)

# This function Is to be used to generate a JWT token when Logging in or Creating an acc Or refreshing the token


def generate_token(payload: dict, expires_delta: timedelta |None = None):
    to_encode = payload.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=TOKEN_EXPIRE_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Secret_key, algorithm=ALGORITHM)
    return encoded_jwt


# This function reads the token and returns the payload and checks the expiry


def decode_token(token: str):
    try:
        data = jwt.decode_complete(
            token, key=Secret_key, algorithms=[ALGORITHM])
        payload = data["payload"]
        header = data["header"]
        if header.get("alg") != ALGORITHM:
            raise HTTPException(
                status_code=401, detail="Invalid Token")
        user_id:str = payload["sub"]

    except ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=401, detail="Token Has Expired") from exc
    except InvalidTokenError as exc:
        raise HTTPException(status_code=403, detail="Invalid Token") from exc
    return user_id


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(getdb)]):
    user_id: str = decode_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid Token")
    user = db.scalars(Select(User).where(User.uuid == user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
