"Pydantic schemas/models"

from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel


class CategoryBaseSchema(BaseModel):
    "Base category schema"
    name: str

class CategorySwaggerSchema(CategoryBaseSchema):
    "Schema for swagger documentation"

    class Config:
        "config"
        from_attributes = True

class CategorySchema(CategoryBaseSchema):
    "Schema for creation and swagger response model"
    id: str

    class Config:
        "config"
        from_attributes = True



class ProductBaseSchema(BaseModel):
    "Base product schema"
    name: str
    description: str | None = None
    price: Decimal | None = Decimal(10.00)
    discount: int | None = 0
    quantity: int | None = 0
    category_id: str | None = None


class CreateProductSchema(ProductBaseSchema):
    "Schema for product creation"
    id: str
    image: str | None = None

    class Config:
        "config"
        from_attributes = True

class ProductFormSwaggerSchema(ProductBaseSchema):
    "Schema for swagger form creation"
    image: str | None = None

    class Config:
        "config"
        from_attributes = True

class ProductJsonSwaggerSchema(ProductBaseSchema):
    "Schema for swagger json creation"
    image_base64: bytes | None = None
    image_name: str | None = None

    class Config:
        "config"
        from_attributes = True

class ProductSchema(ProductBaseSchema):
    "Schema for swagger response model"
    id: str
    image: str | None = None
    date_created: datetime

    class Config:
        "config"
        from_attributes = True


class ProductJsonSwaggerUpdateSchema(BaseModel):
    "Schema for swagger json update"
    name: str
    description: str | None = None
    price: Decimal | None = None
    discount: int | None = None
    quantity: int | None = None
    category_id: str | None = None
    image_base64: bytes | None = None
    image_name: str | None = None

    class Config:
        "config"
        from_attributes = True
