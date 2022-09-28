from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, DATETIME
from sqlalchemy.orm import relationship
from config.base_class import Base

if TYPE_CHECKING:
    from .item import Item


class User(Base):
    __tablename__ = "api_user"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=False)
    is_superuser = Column(Boolean(), default=False)
    items = relationship("Item", back_populates="owner",
                         primaryjoin="User.id==Item.owner_id")
