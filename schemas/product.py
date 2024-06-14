"Pydantic schemas/models"

from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel

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
        orm_mode = True

class ProductFormSwaggerSchema(ProductBaseSchema):
    "Schema for swagger form creation"
    image: str | None = None

    class Config:
        "config"
        orm_mode = True

class ProductJsonSwaggerSchema(ProductBaseSchema):
    "Schema for swagger json creation"
    image_base64: bytes | None = None
    image_name: str | None = None

    class Config:
        "config"
        orm_mode = True

class ProductSchema(ProductBaseSchema):
    "Schema for swagger response model"
    id: str
    image: str | None = None
    date_created: datetime

    class Config:
        "config"
        orm_mode = True
