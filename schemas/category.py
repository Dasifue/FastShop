"Pydantic schemas/models"

from pydantic import BaseModel

class CategoryBaseSchema(BaseModel):
    "Base category schema"
    name: str

class CategorySwaggerSchema(CategoryBaseSchema):
    "Schema for swagger documentation"

    class Config:
        "config"
        orm_mode = True

class CategorySchema(CategoryBaseSchema):
    "Schema for creation and swagger response model"
    id: str

    class Config:
        "config"
        orm_mode = True
