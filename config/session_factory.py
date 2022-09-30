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

engine = create_async_engine(f"{SQLALCHEMY_DATABASE_URL}", pool_size=10, echo=True, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


async def executing__(db: Database, sql: str) -> Any:
    await db.connect()
    result = await db.fetch_all(query=sql, values=None)
    return result


