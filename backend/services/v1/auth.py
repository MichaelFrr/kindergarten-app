
from fastapi import Depends, HTTPException, APIRouter, Response, Body
from backend.schemas import UserResponse, UserCreate,RefreshToken, UserLogin, LoginToken, Token
from backend.database import getdb, Session, Select, or_
from backend.models import User
from typing import Annotated
from backend.dependencies import jwt, InvalidTokenError,ALGORITHM, Secret_key, oauth2_scheme, generate_token, get_pass_hash, verify_password, get_current_user, get_refresh, set_refresh_token

router = APIRouter(tags=["Auth_V1"])


@router.post("/register", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(getdb)):
    email = db.scalars(Select(User.email).where(
        User.email == user.email)).first()
    if email:
        raise HTTPException(status_code=409, detail="User Already Exists")
    hashed_pass = get_pass_hash(user.password)
    new_user = User(
        **user.model_dump(exclude={"password"}), password=hashed_pass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(getdb)):

    query = (Select(User).where(User.email == user.email))
    user_login = db.scalars(query).first()
    if not user_login:
        raise HTTPException(status_code=404, detail="User Does Not Exist")
    password = user_login.password
    uuid = user_login.uuid
    email = user_login.email
    verification = verify_password(user.password, password)

    if not verification:
        raise HTTPException(
            status_code=401, detail="Invalid Email Or Password")
    else:
        payload = {"sub": str(uuid), "email": email}
        access_token = generate_token(payload)
        refresh = set_refresh_token(uuid)
        return LoginToken(access_token=access_token,refresh_token = refresh, token_type="bearer")


##Temporary Refresh Logic Until Learning Http Cookies
@router.post("/refresh")
def refresh_token(body: RefreshToken, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(getdb)):

    try:
        payload = jwt.decode(token, key=Secret_key, algorithms=[ALGORITHM], options={"verify_exp": False})
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid Access Token")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid Access Token ")
    
    stored_refresh = get_refresh(user_id)
    if not stored_refresh or stored_refresh != body.refresh_token:
        raise HTTPException(status_code=401, detail="Invalid Or Expired Refresh Token")
        
    user = db.scalars(Select(User).where(User.uuid == user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")



    new_payload = {"sub": str(user.uuid), "email": user.email}
    new_token = generate_token(new_payload)
    return Token(access_token=new_token, token_type="bearer")