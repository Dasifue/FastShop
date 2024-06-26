"Module for products and categories routes"

import uuid
import base64
from decimal import Decimal

from fastapi import APIRouter, Form, HTTPException, UploadFile, File

from src.database import session
from src.utils import (
    download_image_base64,
    download_image,
)

from .schemas import (
    CategorySchema,
    CategorySwaggerSchema,
    ProductSchema,
    CreateProductSchema,
    ProductJsonSwaggerSchema,
    ProductJsonSwaggerUpdateSchema,
)

from .manager import CategoryCRUD, ProductCRUD


# CATEGORY ENDPOINTS

category_router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)

@category_router.get("/list/", response_model=list[CategorySchema])
async def read_categories(skip: int = 0, limit: int = 100):
    "Endpoint returns an array of categories"
    return await CategoryCRUD.get_many(
        skip=skip,
        limit=limit,
        async_session=session
    )


@category_router.get("/{category_id}", response_model=CategorySchema)
async def read_category(category_id: str):
    "Endpoint returns a category instance"
    result = await CategoryCRUD.get_one(
        category_id=category_id,
        async_session=session
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return result


@category_router.post("/add/json/", response_model=CategorySchema)
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


@category_router.post("/add/form/", response_model=CategorySchema)
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


@category_router.put("/update/form/{category_id}", response_model=CategorySchema)
async def update_category_by_form(category_id: str, name: str = Form()):
    "Endpoint updates a category instance"
    category = CategorySchema(
        id=category_id,
        name=name,
    )
    category_response = await CategoryCRUD.update(
        category=category,
        async_session=session
    )
    return category_response


@category_router.put("/update/json/{category_id}", response_model=CategorySchema)
async def update_category_by_json(category_id: str, category_data: CategorySwaggerSchema):
    "Endpoint updates a category instance"
    category = CategorySchema(
        id=category_id,
        name=category_data.name,
    )
    category_response = await CategoryCRUD.update(
        category=category,
        async_session=session
    )
    return category_response


@category_router.delete("/delete/{category_id}", response_model=dict)
async def delete_category(category_id: str):
    "Endpoint deletes a category instance"
    await CategoryCRUD().delete(
        category_id=category_id,
        async_session=session
    )
    return {"message": "Deleted"}



# PRODUCT ENDPOINTS

product_router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@product_router.get("/list/", response_model=list[ProductSchema])
async def read_products(skip: int = 0, limit: int = 100):
    "Endpoint returns an array of products"
    return await ProductCRUD().get_many(
        skip=skip,
        limit=limit,
        async_session=session
    )


@product_router.get("/{product_id}", response_model=ProductSchema)
async def read_product(product_id: str):
    "Endpoint returns a product instance"
    product = await ProductCRUD().get_one(
        product_id=product_id,
        async_session=session
    )
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@product_router.post("/add/json/", response_model=ProductSchema)
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


@product_router.post("/add/form/", response_model=ProductSchema)
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


@product_router.put("/update/form/{product_id}", response_model=ProductSchema)
async def update_product_by_form(
    product_id: str,
    name: str = Form(),
    description: str | None = Form(None),
    price: Decimal | None = Form(None),
    discount: int | None = Form(None),
    quantity: int | None = Form(None),
    category_id: str = Form(...),
    image: UploadFile | None = File(None)
):
    "Endpoint updates a category instance"
    image_path = None
    if image:
        image_path = await download_image(image.file.read(), f"{uuid.uuid4()}-{image.filename}")
    product = CreateProductSchema(
        id=product_id,
        name=name,
        description=description,
        price=price,
        discount=discount,
        quantity=quantity,
        category_id=category_id,
        image=image_path,
    )
    product_response = await ProductCRUD.update(
        product=product,
        async_session=session
    )
    return product_response


@product_router.put("/update/json/{product_id}", response_model=ProductSchema)
async def update_product_by_json(product_id: str, product_data: ProductJsonSwaggerUpdateSchema):
    "Endpoint updates a category instance"
    image_path = None
    if product_data.image_base64 and product_data.image_name:
        image_data = base64.b64decode(product_data.image_base64)
        image_name = f"{uuid.uuid4()}-{product_data.image_name}"
        image_path = await download_image_base64(bytes_data=image_data, file_name=image_name)

    product = CreateProductSchema(
        id=product_id,
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        discount=product_data.discount,
        quantity=product_data.quantity,
        category_id=product_data.category_id,
        image=image_path
    )
    product_response = await ProductCRUD().update(
        product=product,
        async_session=session
    )
    return product_response


@product_router.delete("/delete/{product_id}", response_model=dict)
async def delete_product(product_id: str):
    "Endpoint deletes a prooduct instance"
    await ProductCRUD().delete(
        product_id=product_id,
        async_session=session
    )
    return {"message": "Deleted"}
