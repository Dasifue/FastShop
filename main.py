"Main project file with base roots"

import asyncio
import argparse
import uuid
import base64
from decimal import Decimal

import uvicorn
from fastapi import FastAPI, HTTPException, Form, UploadFile, File

from database import create_tables, download_image, download_image_base64, session
from database.crud import CategoryCRUD, ProductCRUD
from schemas.category import CategorySchema, CategorySwaggerSchema
from schemas.product import (
    ProductJsonSwaggerSchema,
    CreateProductSchema,
    ProductSchema,
)

app = FastAPI(
    title="FastApi Products",
    description="Simple pet project",
    docs_url="/"
)


# CATEGORY ENDPOINTS

@app.get("/category/list/", response_model=list[CategorySchema])
async def read_categories(skip: int = 0, limit: int = 100):
    "Endpoint returns an array of categories"
    return await CategoryCRUD.get_many(
        skip=skip,
        limit=limit,
        async_session=session
    )


@app.get("/category/{category_id}", response_model=CategorySchema)
async def read_category(category_id: str):
    "Endpoint returns a category instance"
    result = await CategoryCRUD.get_one(
        category_id=category_id,
        async_session=session
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return result


@app.post("/category/add/json/", response_model=CategorySchema)
async def create_category_by_json(category_data: CategorySwaggerSchema):
    "Endpoint creates a category instance"
    category = CategorySchema(
        id=str(uuid.uuid4()),
        name=category_data.name
    )
    categoty_reponse = await CategoryCRUD.create(
        category=category,
        async_session=session
    )
    return categoty_reponse


@app.post("/category/add/form/", response_model=CategorySchema)
async def create_category_by_form(name: str = Form()):
    "Endpoint creates a category instance"
    category = CategorySchema(
        id=str(uuid.uuid4()),
        name=name
    )
    categoty_reponse = await CategoryCRUD.create(
        category=category,
        async_session=session
    )
    return categoty_reponse


@app.delete("/category/delete/{category_id}", response_model=dict)
async def delete_category(category_id: str):
    "Endpoint deletes a category instance"
    await CategoryCRUD().delete(
        category_id=category_id,
        async_session=session
    )
    return {"message": "Deleted"}


# PRODUCT ENDPOINS

@app.get("/product/list/", response_model=list[ProductSchema])
async def read_products(skip: int = 0, limit: int = 100):
    "Endpoint returns an array of products"
    return await ProductCRUD().get_many(
        skip=skip,
        limit=limit,
        async_session=session
    )


@app.get("/product/{product_id}", response_model=ProductSchema)
async def read_product(product_id: str):
    "Endpoint returns a product instance"
    product = await ProductCRUD().get_one(
        product_id=product_id,
        async_session=session
    )
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/product/add/json/", response_model=ProductSchema)
async def create_product_by_json(product_data: ProductJsonSwaggerSchema):
    "Endpoint for creating a product instance"
    image_path = None
    if product_data.image_base64 and product_data.image_name:
        image_data = base64.b64decode(product_data.image_base64)
        image_name = f"{uuid.uuid4()}-{product_data.image_name}"
        image_path = await download_image_base64(bytes_data=image_data, file_name=image_name)

    product = CreateProductSchema(
        id=str(uuid.uuid4()),
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        discount=product_data.discount,
        quantity=product_data.quantity,
        category_id=product_data.category_id,
        image=image_path
    )
    product_response = await ProductCRUD().create(
        product=product,
        async_session=session
    )
    return product_response


@app.post("/product/add/form/", response_model=ProductSchema)
async def create_product_by_form(
    name: str = Form(...),
    description: str | None = Form(None),
    price: Decimal | None = Form(Decimal(10.00), ge=0),
    discount: int | None = Form(0, ge=0, le=100),
    quantity: int | None = Form(0, ge=0),
    category_id: str = Form(...),
    image: UploadFile | None = File(None)
):
    "Endpoint for creating a product instance"
    if image:
        image_path = await download_image(image.file.read(), f"{uuid.uuid4()}-{image.filename}")
    product = CreateProductSchema(
        id=str(uuid.uuid4()),
        name=name,
        description=description,
        price=price,
        discount=discount,
        quantity=quantity,
        category_id=category_id,
        image=image_path,
    )
    product_response = await ProductCRUD().create(
        product=product,
        async_session=session
    )
    return product_response




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Using with database")
    parser.add_argument("extra", nargs="?", default=None)
    args = parser.parse_args()

    if args.extra == "create_tables":
        asyncio.run(create_tables())

    uvicorn.run(
        app=app,
        host="127.0.0.1",
        port=8000
    )