from backend.services.v1 import public, users, user_child
from backend.services.v1.internal.managmet import children, classrooms
from fastapi import APIRouter

v1_router = APIRouter()

v1_router.include_router(user_child.router, prefix="/child")
v1_router.include_router(users.router, prefix="/users")
v1_router.include_router(public.router, prefix="/public")
v1_router.include_router(children.router, prefix="/management/children")
v1_router.include_router(classrooms.router, prefix="/management/classrooms")
