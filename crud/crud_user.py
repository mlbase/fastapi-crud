from typing import Any, Dict, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

import model
from config.security import get_password_hash, verify_password
from crud.base import CRUDBase
from model.user import User
from schema.user import UserCreate, UserUpdate, UserWithItem
from sqlalchemy.exc import NoResultFound


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, session: AsyncSession, *, email: str) -> User | None:
        statement = select(User).where(User.email == email)

        q_object = await session.execute(statement=statement, params={"email_1": email})
        return q_object.scalars().first()

    async def create(self, session: AsyncSession, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name
        )

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self, session: AsyncSession, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["paasword"]
            update_data["hashed_password"] = hashed_password
        return await super().update(session=session, db_obj=db_obj, obj_in=update_data)

    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> User | None:
        user = self.get_by_email(db, email=email)
        print(user)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return await user

    async def is_active(self, user: User) -> bool:
        return await user.is_active

    async def get_by_id(self, session: AsyncSession, id: int) -> None:
        statement = select(model.User).options(selectinload(model.User.items))\
            .filter(model.User.id == id)

        q_object = await session.execute(statement=statement)
        result = q_object.scalar()
        return result

    async def get_by_id_raw(self, session: AsyncSession, id: int) -> None:
        statement1 = "SELECT api_user.* " \
                     "FROM api_user " \
                     "WHERE api_user.id = :id_1"
        statement2 = "SELECT item.* " \
                     "FROM item " \
                     "WHERE item.owner_id = :id_2"

        q_object1 = await session.execute(statement=statement1, params={"id_1": id})
        q_object2 = await session.execute(statement=statement2, params={"id_2": id})
        user_data = q_object1.first()
        print(user_data)
        item_data = q_object2.all()
        print(item_data)
        print(user_data)
        print(item_data)
        result = UserWithItem(**user_data, items=item_data)
        return result

user = CRUDUser(User)
