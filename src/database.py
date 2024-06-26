"Async database connection module"

import os

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv

load_dotenv(".env")

class Base(DeclarativeBase):
    "class for sqlalchemy ORM system"


DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    engine = create_async_engine(
        url=DATABASE_URL,
        echo=True
    )
    session = async_sessionmaker(
        bind=engine,
        expire_on_commit=True
    )
else:

    class DatabaseConnectionError(Exception):
        "Exception class"

    raise DatabaseConnectionError("Database connection URL not specified!")
