from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from config.base_class import Base

if TYPE_CHECKING:
    from .user import User


class Item(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(String, ForeignKey("user.py.id"))
    owner = relationship("User", back_populates="items")