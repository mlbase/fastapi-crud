from sqlalchemy import create_engine, future
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from dotenv import load_dotenv
from sqlalchemy.sql import table, column, select
from databases import Database
from typing import Any
import asyncio
import logging
import os
import model

load_dotenv()
DB_USERNAME: str = os.getenv("DB_USERNAME")
DB_PASSWORD: str = os.getenv("DB_PASSWORD")
DB_HOST: str = os.getenv("DB_HOST")
DB_PORT: str = os.getenv("DB_PORT")
DB_DATABASE: str = os.getenv("DB_DATABASE")
SQLALCHEMY_DATABASE_URL: str = f"mysql+aiomysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

engine = create_engine(f"{SQLALCHEMY_DATABASE_URL}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


'''
    asyncio 를 이용한 경우
'''
# async def async_main():
#     async_engine = create_async_engine(
#         SQLALCHEMY_DATABASE_URL, echo=True
#     )
#
#     async_session = sessionmaker(
#         async_engine, expire_on_commit=False, class_=AsyncSession
#     )
#     async with async_session() as session:
#         stmt = select(model.User)
#         print(stmt)
#         result = await session.execute(stmt)
#         await session.commit()
#     return
#
# if __name__ == '__main__':
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop=loop)
#     task = asyncio.create_task(async_main())
#     asyncio.run(task)


async def executing__(db: Database, sql: str) -> Any:
    await db.connect()
    result = await db.fetch_all(query=sql, values=None)
    return result


if __name__ == '__main__':
    database = Database(f"{SQLALCHEMY_DATABASE_URL}")
    print('='*40)
    stmt = select(model.User).filter()
    print(stmt)
    loop = asyncio.get_event_loop()
    try:
        rs = loop.run_until_complete(executing__(db=database, sql=stmt))
    except RuntimeError:
        pass
    loop.close()
    print('='*40)
    print(rs)
