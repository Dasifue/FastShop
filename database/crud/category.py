"CRUD for category model"

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.sql.schema import Sequence
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from database.models import Category
from schemas import category as ct


class CategoryCRUD:
    "CRUD operations class for category"

    @classmethod
    async def get_many(
        cls,
        async_session: async_sessionmaker[AsyncSession],
        skip: int = 0,
        limit: int = 100
        ) -> Sequence[Category]:  # type: ignore
        "Coroutine for getting array of categories"
        async with async_session() as session:
            result = await session.execute(
                select(Category).offset(skip).limit(limit)
            )

            return result.scalars().all()  # type: ignore

    @classmethod
    async def get_one(
        cls,
        category_id: str,
        async_session: async_sessionmaker[AsyncSession]
        ) -> Category | None:
        "Coroutine for getting an category instance"
        async with async_session() as session:
            result = await session.execute(
                select(Category).filter(Category.id==category_id)
            )
            return result.scalar_one_or_none()

    @classmethod
    async def create(
        cls,
        category: ct.CategorySchema,
        async_session: async_sessionmaker[AsyncSession]
    ) -> Category:
        "Coroutine for creating an category instance"
        async with async_session() as session:
            db_category = Category(**category.dict())
            session.add(db_category)
            try:
                await session.commit()
            except IntegrityError as error:
                raise HTTPException(
                    status_code=400,
                    detail="Category with this name already exists"
                ) from error
            await session.refresh(db_category)
            return db_category


    @classmethod
    async def delete(
        cls,
        category_id: str,
        async_session: async_sessionmaker[AsyncSession]
    ) -> None:
        "Coroutine for deleting an category instance"
        async with async_session() as session:
            category = await cls.get_one(
                category_id=category_id,
                async_session=async_session
            )
            if category:
                await session.delete(instance=category)
            else:
                raise HTTPException(
                    status_code=404,
                    detail="Category not found"
                )
            await session.commit()
