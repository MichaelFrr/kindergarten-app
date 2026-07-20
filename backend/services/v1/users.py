from fastapi import FastAPI, Depends, HTTPException, APIRouter
from backend.schemas import UserResponse, UserCreate
from backend.database import getdb, Base, engine, Session
from backend.models import User

router = APIRouter(tags=["User_V1"])


@router.get("/users",)
def get_users(limit=10, db: Session = Depends(getdb)):
    users = db.query(User).limit(limit).all()
    if not users:
        raise HTTPException(status_code=404, detail="Users does not exist")
    return users


@router.get("/user/{user_name}")
def get_user_by_name(user_name: str, db: Session = Depends(getdb)):
    first_name = db.query(User).filter(User.first_name == user_name).first()
    last_name = db.query(User).filter(User.last_name == user_name)
    if not first_name:
        raise HTTPException(status_code=404, detail="User Does Not Exist!")
    return first_name


@router.post("/user", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(getdb)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=404, detail="User Already Exists")
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
