from unittest import TestCase, mock
from utils.dependencies import get_db
from config.session_factory import engine
from sqlalchemy.ext.asyncio import AsyncSession
from crud.crud_item import item


class Test(TestCase):
    def setUp(self) -> None:
        session = AsyncSession(engine)
        self.session = session
        self.crud = item

    async def test_runs(self):
        self.session = get_db(self.session)
        result = await item.get_multi(self.session)
        print(result)
        assert result is None
