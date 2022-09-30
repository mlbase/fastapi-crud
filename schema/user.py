from pydantic import BaseModel, EmailStr, Field
from typing import List
from schema.item import ItemInDB


# Shared properties
class UserBase(BaseModel):
    email: EmailStr | None = Field(example="email id@domain.com")
    is_active: bool | None = Field(example="사용 여부")
    full_name: str | None = Field(example="사용 이름")

    class Config:
        schema_extra = {
            "email": "user@example.com",
            "is_active": True,
            "full_name": "example name",
            "items": [
                {
                    "title": "item title",
                    "description": "this item is..."
                }
            ]
        }


class UserCreate(UserBase):
    email: EmailStr = Field(example="id@domain.com")
    password: str = Field(example="비밀번호")


class UserUpdate(UserBase):
    password: str | None = Field(example="비밀번호")


class UserInDBBase(UserBase):
    id: int | None = Field("db index")

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str


class UserWithItem(UserBase):
    items: List[ItemInDB] | None

    class Config:
        orm_mode = True
