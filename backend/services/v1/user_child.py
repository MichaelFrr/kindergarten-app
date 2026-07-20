from backend.schemas import UserResponse, UserCreate
from backend.database import getdb, Base, engine, Session
from backend.models import User
from fastapi import Depends, HTTPException, APIRouter

router = APIRouter(tags=["User_Child_V1"])


@router.get("/test")
def test():
    return {"heyyy."}
