from fastapi import Depends, HTTPException, APIRouter, Response
from backend.schemas import UserResponse
from backend.database import getdb, Session, Select, or_
from backend.models import User
from typing import Annotated
from backend.dependencies import get_current_user


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


@router.get("/me")
def test_token(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/all")
def get_all(db: Session = Depends(getdb)):
    query = Select(User)
    users = db.scalars(query).all()
    return(users)
