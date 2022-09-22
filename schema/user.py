from pydantic import BaseModel, EmailStr, Field


#Shared properties
class UserBase(BaseModel):
    email: EmailStr | None = Field(description="email id@domain.com")
    is_active: bool | None = Field(str="사용 여부")
    full_name: str | None = Field(default="사용 이름")


class UserCreate(UserBase):
    email: EmailStr = Field(s="id@domain.com")
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