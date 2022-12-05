# pip dependency
from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from starlette.requests import Request
from starlette.authentication import requires
import databases
import logging
# local dependency
import crud
from crud.crud_user import user
import model
import schema
from utils.dependencies import get_db, get_current_user
from config import security
from config.setting import settings
from config.session_factory import SQLALCHEMY_DATABASE_URL
from custom_exception.Exceptions import InvalidateUserException, SQLException

router = APIRouter()

database = databases.Database(SQLALCHEMY_DATABASE_URL)
logging.basicConfig()
logging.getLogger("database.Database").setLevel(logging.INFO)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="access_token")


@router.post("/access_token",
             response_model=schema.Token,
             responses={
                 200: {
                     "model": schema.Token,
                     "description": "jwt response successfully",
                     "content": {
                         "application/json": {
                             "example": {
                                 "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHA...",
                                 "token_type": "Bearer"
                             },
                             "schema": {
                                 "access_token": "jwt 토큰",
                                 "token_type": "베어러 타입"
                             }
                         }
                     }
                 },
                 400: {"description": "Incorrect email or password"}
             },
             summary="토큰발급 api"
             )
async def login_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
) -> Any:
    # with Session(engine) as session: sync 일 경우
    query = select(model.User).filter(model.User.email == form_data.username)
    try:
        query_result = await db.execute(query)
        current_user = query_result.first().User
    except SQLAlchemyError as ex:
        raise ex
    password_check = security.verify_password(plain_password=form_data.password,
                                              hashed_password=current_user.hashed_password)
    if not password_check:
        raise InvalidateUserException
    elif not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            subject=current_user.id, expires_delta=access_token_expires, superuser_check=current_user.is_superuser
        ),
        "token_type": "bearer",
    }


@router.post("/test_token", response_model=schema.User)
@requires(["authenticated"])
def test_token(
        request: Request,
        token=Depends(oauth2_scheme)
) -> Any:
    current_user = request.user
    return current_user


@router.get("/",
            response_model=schema.UserWithItem,
            responses={
                200: {
                    "model": schema.UserWithItem,
                    "description": "my page response successfully",
                    "content": {
                        "application/json": {
                            "example": {
                                "email": "user@example.com",
                                "is_active": True,
                                "full_name": "example name",
                                "items": [
                                    {
                                        "title": "item title",
                                        "description": "this item is..."
                                    }
                                ]
                            },
                            "schema": {
                                "email": "user의 email",
                                "is_active": "활성화 되어 있는지 여부 boolean",
                                "full_name": "user의 이름",
                                "items": "item에 대한 리스트"
                            }
                        }
                    }
                }
            }
            )
@requires(["authenticated", "admin"])
async def user_my_page(
        # current_user: model.User = Depends(get_current_user),
        token=Depends(oauth2_scheme),
        *,
        request: Request
) -> Any:
    # current_id = current_user.id
    # result = await user.get_by_id_raw(session, current_id)
    # print(response)
    result = request.user
    return result
