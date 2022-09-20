from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import model
import schema
from utils import dependencies

router = APIRouter()


@router.get("/", response_model=List[schema.Item])
def read_items(
    db: Session = Depends(dependencies.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: model.User = Depends(dependencies.get_current_user)
) -> Any:

    if current_user:
        items = crud.item.get_multi(db, skip=skip, limit=limit)
    else:
        items = crud.item.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )

    return items


@router.post("/", response_model=schema.Item)
def create_item(
    *,
    db: Session = Depends(dependencies.get_db),
    item_in: schema.ItemCreate,
    current_user: model.user = Depends(dependencies.get_current_user),
) -> Any:
    item = crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
    return item


@router.put("/{id}", response_model=schema.Item)
def update_item(
    *,
    db: Session = Depends(dependencies.get_db),
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
    db: Session = Depends(dependencies.get_db),
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
    db: Session = Depends(dependencies.get_db),
    id: int,
    current_user: model.User = Depends(dependencies.get_current_user)
) -> Any:
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = crud.item.remove(db=db, id=id)
    return item