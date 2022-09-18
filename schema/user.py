from pydantic import BaseModel, EmailStr


#Shared properties
class UserBase(BaseModel):
    email: EmailStr | None
    is_active: bool | None
    full_name: str | None


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: str | None


class UserInDBBase(UserBase):
    id: int | None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str