from fastapi import APIRouter

from api.v1 import user_api

api_router = APIRouter()
api_router.include_router(user_api.router, prefix="/user.py", tags=["users"])