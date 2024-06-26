"Database models"

from decimal import Decimal
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Category(Base):
    "product category model"

    __tablename__ = "category"
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    products: Mapped[list["Product"]] = relationship(back_populates="category")

    def __repr__(self) -> str:
        return f"<Category.{self.name}: {self.id}>"

class Product(Base):
    "main product model"

    __tablename__ = "product"
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    image: Mapped[str] = mapped_column(default="/media/default/products.png")
    price: Mapped[Decimal] = mapped_column(default=Decimal(10.00))
    discount: Mapped[int] = mapped_column(default=0)
    quantity: Mapped[int] = mapped_column(default=0)
    date_created: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    category_id: Mapped[str | None] = mapped_column(ForeignKey("category.id", ondelete="SET NULL"))

    category: Mapped["Category"] = relationship(back_populates="products")

    def __repr__(self) -> str:
        return f"<Product.{self.name}: {self.id}>"
