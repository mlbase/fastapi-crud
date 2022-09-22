from typing import Generator

import model
import crud
import databases
from sqlalchemy.sql import select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from config.session_factory import SessionLocal, SQLALCHEMY_DATABASE_URL
from schema.user import UserCreate, User, UserUpdate
from schema.token import Token, TokenPayload
from config import security
from config.setting import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

database = databases.Database(SQLALCHEMY_DATABASE_URL)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> model.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data= TokenPayload(**payload)
    except (ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    print(token_data.sub)
    id: int = token_data.sub
    query = select(model.User).where(model.User.id == id)
    print(query)
    await database.connect()
    user = await database.fetch_one(query=query)
    print(user)
    await database.disconnect()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="test@test.com", full_name="test"
    )