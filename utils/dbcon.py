import model
import crud
from config.session_factory import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends
from schema.user import UserCreate, User, UserUpdate


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db)) -> model.User:
    user = crud.user.get_by_email(db=db, email="test@test.com")
    if not user:
        user_in = UserCreate.parse_obj({'email': 'test@test.com', 'password': '1234', 'full_name': 'testing..'})
        user = crud.user.create(db=db, obj_in=user_in)

    return user
