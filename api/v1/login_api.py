from datetime import timedelta
from typing import Any
from pydantic import BaseModel
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import databases
from sqlalchemy.sql import table, select
import model
import crud
import model
import schema
from utils import dependencies
from config import security
from config.security import get_password_hash
from config.setting import settings
from config.session_factory import engine, SQLALCHEMY_DATABASE_URL
import logging

router = APIRouter()

database = databases.Database(SQLALCHEMY_DATABASE_URL)
logging.basicConfig()
logging.getLogger("database.Database").setLevel(logging.INFO)


@router.post("/access-token",
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
                                }
                            }
                        }
                       },
                 400: {"description": "authentication failed"}
             },
             summary="토큰발급 api"
             )
async def login_access_token(
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    # with Session(engine) as session: sync 일 경우

    query = """
            SELECT *
            FROM api_user
            WHERE api_user.email = :email
            """
    # query = select(model.User).filter(model.User.email)
    # print(query)
    try:
        await database.connect()
        print("connection start")
        user = await database.fetch_one(query=query, values={"email": form_data.username})
        print(user)
    except ConnectionRefusedError:
        raise HTTPException(status_code=503, detail="Too many Request")
    finally:
        print("fetching end...")
        await database.disconnect()
    print("connection end")
    password_check = security.verify_password(plain_password=form_data.password, hashed_password=user.hashed_password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not password_check:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            subject=user.id, expires_delta=access_token_expires, superuser_check=user.is_superuser
        ),
        "token_type": "bearer",
    }


@router.post("/test-token", response_model=schema.User)
def test_token(current_user: model.User = Depends(dependencies.get_current_user)) -> Any:
    return current_user
