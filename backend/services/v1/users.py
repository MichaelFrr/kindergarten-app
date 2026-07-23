from fastapi import FastAPI, Depends, HTTPException, APIRouter, Response
from fastapi.security import OAuth2AuthorizationCodeBearer
from backend.schemas import UserResponse, UserCreate, UserLogin
from backend.database import getdb, Base, engine, Session, Select
from backend.models import User
from backend.dependencies import pass_hash, generate_token, decode_token, get_pass_hash, verify_password

router = APIRouter(tags=["User_V1"])


@router.get("/user/{user_name}")
def get_user_by_name(user_name: str, db: Session = Depends(getdb)):
    first_name = db.query(User).filter(User.first_name == user_name).first()
    last_name = db.query(User).filter(User.last_name == user_name).first()
    if not first_name or last_name:
        raise HTTPException(status_code=404, detail="User Does Not Exist!")
    return first_name


@router.post("/register", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(getdb)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=409, detail="User Already Exists")
    hash = get_pass_hash(user.password)
    user.password = hash
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(getdb)):
    email = db.scalars(Select(User.email).where(
        User.email == user.email)).first()
    password = db.scalars(Select(User.password).where(
        User.email == user.email)).first()
    id = db.scalars(Select(User.uuid).where(User.email == user.email)).first()
    if password is None:
        raise HTTPException(
            status_code=401, detail="Invalid Email Or Password")

    verification = verify_password(user.password, password)

    if not email:
        raise HTTPException(
            status_code=401, detail="Invalid Email Or Password")
    if not verification:
        raise HTTPException(
            status_code=401, detail="Invalid Email Or Password")
    else:
        payload = {"sub": user.email}
        res = generate_token(payload)
        return {"access_token": res, "token_type": "bearer"}
