from fastapi import FastAPI, Depends, HTTPException, APIRouter, Response
from backend.schemas import UserResponse, UserCreate
from backend.database import getdb, Base, engine, Session
from backend.models import User
from backend.dependencies import pass_hash

router = APIRouter(tags=["User_V1"])


@router.get("/user/{user_name}")
def get_user_by_name(user_name: str, db: Session = Depends(getdb)):
    first_name = db.query(User).filter(User.first_name == user_name).first()
    last_name = db.query(User).filter(User.last_name == user_name).first()
    if not first_name or last_name:
        raise HTTPException(status_code=404, detail="User Does Not Exist!")
    return first_name


@router.post("/user", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(getdb)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=409, detail="User Already Exists")
    hash = pass_hash.hash(user.password)
    user.password = hash
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
