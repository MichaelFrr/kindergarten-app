from fastapi import Depends, HTTPException, APIRouter, Response
from backend.schemas import UserResponse, UserCreate, UserLogin, Token
from backend.database import getdb, Session, Select, or_
from backend.models import User
from typing import Annotated
from backend.dependencies import generate_token, decode_token, get_pass_hash, verify_password, get_current_user


router = APIRouter(tags=["User_V1"])


@router.get("/user/{user_name}")
def get_user_by_name(user_name: str, db: Session = Depends(getdb)):
    query = (Select(User).where(
        or_(User.first_name == user_name, User.last_name == user_name)))
    user = db.scalars(query).first()
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid Email Or Password")
    return user


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
        return Token(access_token=access_token, token_type="bearer")


@router.get("/me")
def test_token(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@router.post("/refresh")
def refresh_token():
    pass

@router.get("/all")
def get_all(db: Session = Depends(getdb)):
    query = Select(User)
    users = db.scalars(query).all()
    return(users)