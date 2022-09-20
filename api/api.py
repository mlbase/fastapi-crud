from fastapi import APIRouter

from api.v1 import user_api, login_api, item_api

api_router = APIRouter()
api_router.include_router(user_api.router, prefix="/users", tags=["users"])
api_router.include_router(login_api.router, prefix="/logins", tags=["logins"])
api_router.include_router(item_api.router, prefix="/items", tags=["items"])