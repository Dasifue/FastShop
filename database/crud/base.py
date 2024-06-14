"""
Base classes for CRUD operations
IN DEVELOPMENT
"""


from inspect import getmembers
from functools import wraps

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

class CRUDBase:
    "Class for main attributes"
    model = None

    @classmethod
    def check_attrs(cls, func):
        "Decorator for checking atributes are not None"
        @wraps
        async def wrapper(*args, **kwargs):
            for attr, value in reversed(getmembers(cls)):
                if attr.startswith("__") and attr.endswith("__"):
                    break
                if value is None:
                    raise AttributeError(f"Attribute {attr} must have value")
            return await func(*args, **kwargs)
        return wrapper


class GET(CRUDBase):
    "Class for get data from db"

    @classmethod
    @CRUDBase.check_attrs
    async def get_many(
        cls,
        async_session: async_sessionmaker[AsyncSession],
        skip: int = 0,
        limit: int = 100
        ):  # type: ignore
        "Coroutine for getting array of products"
        async with async_session() as session:
            result = await session.execute(
                select(cls.model).offset(skip).limit(limit)
            )

            return result.scalars().all()  # type: ignore

    @classmethod
    @CRUDBase.check_attrs
    async def get_one(
        cls,
        object_id: str,
        async_session: async_sessionmaker[AsyncSession]
        ):
        "Coroutine for getting an category instance"
        async with async_session() as session:
            result = await session.execute(
                select(cls.model).filter(cls.model.id==object_id)
            )
            return result.scalar_one_or_none()


class CREATE(CRUDBase):
    "Class for create data in database"

    @classmethod
    @CRUDBase.check_attrs
    async def create(
        cls,
        object_data: "model_shcema",
        async_session: async_sessionmaker[AsyncSession]
        ):
        "Coroutine for creating an category instance"
        async with async_session() as session:
            db_object = cls.model(**object_data.dict())
            session.add(db_object)
            try:
                await session.commit()
            except IntegrityError as error:
                raise HTTPException(
                    status_code=400,
                    detail="Category with this name already exists"
                ) from error
            await session.refresh(db_object)
            return db_object


class DELETE(CRUDBase):
    "Class for delete data in database"

    @classmethod
    @CRUDBase.check_attrs
    async def delete(
        cls,
        object_id: str,
        async_session: async_sessionmaker[AsyncSession]
        ):
        "Coroutine for deleting an category instance"
        async with async_session() as session:
            db_object = await GET.get_one(
                object_id=object_id,
                async_session=async_session
            )
            if db_object:
                await session.delete(instance=db_object)
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"{cls.model.__tablename__} not found"
                )
            await session.commit()
