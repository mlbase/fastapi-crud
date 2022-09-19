from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
import crud
import model
import schema
from utils.dbcon import get_db, get_current_user

router = APIRouter()


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

    :param db: orm_session
    :param user_in: user that want to create
    :return: User | None
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
def update_user_me(
        *,
        db: Session = Depends(get_db),
        password: str = Body(None),
        full_name: str = Body(None),
        email: EmailStr = Body(None),
        current_user: model.User = Depends(get_current_user)
) -> Any:
    """

    :param db: orm_session
    :param password:
    :param full_name:
    :param email:
    :param current_user: injected by get_current_user, now it is "test"
    :return: User | None
    """

    current_user_data = jsonable_encoder(current_user)
    user_in = schema.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


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
