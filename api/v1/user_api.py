from typing import Any, List

import pydantic
from pydantic import Field
from fastapi import APIRouter, Depends, HTTPException, Body, Response
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import select, update, Table
import crud
import model
import schema
from utils.dependencies import get_db, get_current_user
import databases
from config.session_factory import SQLALCHEMY_DATABASE_URL
from config.security import get_password_hash
from pydantic import BaseModel

import json

database = databases.Database(SQLALCHEMY_DATABASE_URL)
router = APIRouter()


class UpdateUser(BaseModel):
    email: EmailStr = Field(description="요청할 이메일")
    password: str = Field(description="변경할 비밀번호")
    full_name: str = Field(description="변경할 이름")


@router.get("/", response_model=List[schema.User])
def read_users(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """

    :param db: orm_session
    :param skip: offset
    :param limit: rows per page
    :return:
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users
    # return ''


@router.post("/", response_model=schema.User)
def create_user(
        *,
        db: Session = Depends(get_db),
        user_in: schema.UserCreate,
) -> Any:
    """
    # testestset

    - test!00

    ```
        @router.post("/", response_model=schema.User)
def create_user(
        *,
        db: Session = Depends(get_db),
        user_in: schema.UserCreate,
) -> Any:
    ```


    ffffg

    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.put("/me", response_model=schema.User)
async def update_user_me(
        *,
        request: UpdateUser,
        current_user: model.User = Depends(get_current_user)
) -> Any:
    """

    user update 하는 api \n
    bearer-token needed
    """

    current_user_data = jsonable_encoder(current_user)
    user_in = request
    if request.password is not None:
        user_in.password = get_password_hash(password=request.password)
    if request.full_name is not None:
        user_in.full_name = request.full_name
    if request.email is not None:
        user_in.email = request.email
    value_map = dict(email=user_in.email, full_name=user_in.full_name, hashed_password=user_in.password)

    query = """UPDATE api_user 
            SET api_user.full_name = :full_name, api_user.hashed_password = :hashed_password 
            WHERE api_user.email = :email"""

    print(query)
    # TODO with 쓰는것 확인
    async with database as session:
        await session.connect()
        await session.execute(query=query, values=dict(value_map))
        await session.disconnect()
    return Response(status_code=202)
    # return user_in


@router.get("/me", response_model=schema.User)
def read_user_me(
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user)
) -> Any:
    """

    :param db: orm_session
    :param current_user: current user
    :return: User | None
    """
    return current_user


@router.get("/open", response_model=schema.User)
def create_user_open(
    *,
    db: Session = Depends(get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None)
) -> Any:
    """

    :param db: orm_session
    :param password: input
    :param email: input
    :param full_name: input
    :return: User | None
    """
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="the user with this username already exist in the system"
        )
    user_in = schema.UserCreate(password=password, email=email, full_name=full_name)
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.put("/{user_id}", response_model=schema.User)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: schema.UserUpdate,
) -> Any:
    """

    :param db: orm_session
    :param user_id: input via path_variable
    :param user_in: updating dto
    :return:
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="the user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
