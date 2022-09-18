from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.session_factory import engine
import schema, model, crud

router = APIRouter()


@router.get("/", response_model=List[schema.User])
def read_users(
    db: Session,
    skip: int = 0,
    limit : int = 100,
    current_user = model.User
) -> Any:
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schema.User)
def create_user(
    db: Session,
    user_in: schema.UserCreate,
    current_user: model.User
) -> Any:

    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user

