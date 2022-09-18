from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str | None
    description: str | None


class ItemCreate(ItemBase):
    title: str


class ItemUpdate(ItemBase):
    pass


class ItemInDBBase(ItemBase):
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True


class ItemInDB(ItemInDBBase):
    pass


class Item(ItemInDBBase):
    pass