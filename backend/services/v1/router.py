from backend.services.v1 import users, user_child, guest
from backend.services.v1.internal.managmet import children, classrooms
from fastapi import APIRouter

v1_router = APIRouter()

v1_router.include_router(user_child.router, prefix="/child")
v1_router.include_router(users.router, prefix="/users")
v1_router.include_router(guest.router, prefix="/guests")
v1_router.include_router(children.router, prefix="/management/children")
v1_router.include_router(classrooms.router, prefix="/management/classrooms")
