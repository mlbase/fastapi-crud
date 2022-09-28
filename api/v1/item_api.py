from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import model
import schema
from utils import dependencies
import databases
from config.session_factory import SQLALCHEMY_DATABASE_URL

database = databases.Database(SQLALCHEMY_DATABASE_URL)
router = APIRouter()


@router.get("/", response_model=List[schema.Item])
async def read_items(
    skip: int = 0,
    limit: int = 100,
    current_user: model.User = Depends(dependencies.get_current_user)
) -> Any:
    query = "SELECT item.id, item.title, item.description, item.owner_id" \
            + "FROM item JOIN api.user ON item.owner_id = api_user.user_id" \
            + "AND api_user.user_id = :id"
    value_map = {"id": current_user.id}

    async with database:
        await database.connect()
        items = await database.fetch_all(query=query, values=value_map)
        await database.disconnect()
    return items


@router.post("/", response_model=schema.Item)
async def create_item(
    *,
    db: AsyncSession = Depends(dependencies.get_db),
    item_in: schema.ItemCreate,
    current_user: model.user = Depends(dependencies.get_current_user),
) -> Any:
    item = await crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
    return item


@router.put("/{id}", response_model=schema.Item)
def update_item(
    *,
    db: AsyncSession = Depends(dependencies.get_db),
    id: int,
    item_in: schema.ItemUpdate,
    current_user: model.User = Depends(dependencies.get_current_user),
) -> Any:
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = crud.item.update(db=db, db_obj=item, obj_in=item_in)
    return item


@router.get("/{id}", response_model=schema.Item)
def read_item(
    *,
    db: AsyncSession = Depends(dependencies.get_db),
    id: int,
    current_user: model.User = Depends(dependencies.get_current_user)
) -> Any:
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{id}", response_model=schema.Item)
def delete_item(
    *,
    db: AsyncSession = Depends(dependencies.get_db),
    id: int,
    current_user: model.User = Depends(dependencies.get_current_user)
) -> Any:
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = crud.item.remove(db=db, id=id)
    return item