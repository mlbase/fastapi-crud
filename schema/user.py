from pydantic import BaseModel, EmailStr, Field
from typing import List
from schema.item import ItemInDB

#Shared properties
class UserBase(BaseModel):
    email: EmailStr | None = Field(description="email id@domain.com")
    is_active: bool | None = Field(str="사용 여부")
    full_name: str | None = Field(default="사용 이름")


class UserCreate(UserBase):
    email: EmailStr = Field(str="id@domain.com")
    password: str = Field("비밀번호")


class UserUpdate(UserBase):
    password: str | None


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
