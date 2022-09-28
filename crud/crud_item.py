from typing import List, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from crud.base import CRUDBase
from model.item import Item
from schema.item import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    async def create_with_owner(
        self, db: AsyncSession, *, obj_in: ItemCreate, owner_id: int
    ) -> Any:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_owner(
        self, db: AsyncSession, *, owner_id: str, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        return await (
            db.get(self.model)
            .filter(Item.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


item = CRUDItem(Item)