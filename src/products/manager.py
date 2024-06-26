"CRUD for category model"

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.sql.schema import Sequence
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from .models import Category, Product
from .schemas import (
    CategorySchema,
    CreateProductSchema
)


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
        category: CategorySchema,
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
    async def update(
        cls,
        category: CategorySchema,
        async_session: async_sessionmaker[AsyncSession],
    ) -> Category:
        "Couroutine for updating a category instance"
        async with async_session() as session:
            category_rows = await session.execute(
                select(Category).filter(Category.id==category.id)
            )
            category_row = category_rows.scalar_one_or_none()

            if not category_row:
                raise HTTPException(
                        status_code=404,
                        detail="Category not found"
                    )

            category_row.name = category.name
            try:
                await session.commit()
            except IntegrityError as error:
                raise HTTPException(
                    status_code=400,
                    detail="Category with this name already exists"
                ) from error
            await session.refresh(category_row)
            return category_row


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


class ProductCRUD:
    "CRUD operations class for product"

    @classmethod
    async def get_many(
        cls,
        async_session: async_sessionmaker[AsyncSession],
        skip: int = 0,
        limit: int = 100
        ) -> Sequence[Product]:  # type: ignore
        "Coroutine for getting array of products"
        async with async_session() as session:
            result = await session.execute(
                select(Product).offset(skip).limit(limit)
            )

            return result.scalars().all()  # type: ignore

    @classmethod
    async def get_one(
        cls,
        product_id: str,
        async_session: async_sessionmaker[AsyncSession]
        ) -> Product | None:
        "Coroutine for getting an product instance"
        async with async_session() as session:
            result = await session.execute(
                select(Product).filter(Product.id==product_id)
            )
            return result.scalar_one_or_none()

    @classmethod
    async def create(
        cls,
        product: CreateProductSchema,
        async_session: async_sessionmaker[AsyncSession]
    ) -> Product:
        "Coroutine for creating an product instance"
        async with async_session() as session:
            db_category = Product(**product.dict())
            session.add(db_category)
            try:
                await session.commit()
            except IntegrityError as error:
                raise HTTPException(
                    status_code=404,
                    detail=error,
                ) from error
            await session.refresh(db_category)
            return db_category

    @classmethod
    async def update(
        cls,
        product: CreateProductSchema,
        async_session: async_sessionmaker[AsyncSession],
    ) -> Product:
        "Couroutine for updating a product instance"
        async with async_session() as session:
            product_rows = await session.execute(
                select(Product).filter(Product.id==product.id)
            )
            product_row = product_rows.scalar_one_or_none()

            if not product_row:
                raise HTTPException(
                        status_code=404,
                        detail="Product not found"
                    )
            for param, value in product:
                if value is not None:
                    setattr(product_row, param, value)

            try:
                await session.commit()
            except IntegrityError as error:
                raise HTTPException(
                    status_code=404,
                    detail="Category not found"
                ) from error
            await session.refresh(product_row)
            return product_row


    @classmethod
    async def delete(
        cls,
        product_id: str,
        async_session: async_sessionmaker[AsyncSession]
    ) -> None:
        "Coroutine for deleting an product instance"
        async with async_session() as session:
            async with session.begin():
                product = await cls.get_one(
                    product_id=product_id,
                    async_session=async_session
                )
                if product:
                    await session.delete(instance=product)
                else:
                    raise HTTPException(
                        status_code=404,
                        detail="Product not found"
                    )
                await session.commit()
