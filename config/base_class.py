from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str
    __table_args__ = {'extend_existing': True}
    #Generate __tablename__ automatically
    def __tablename__(self) -> str:
        return self.__name__.lower()