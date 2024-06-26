"Main project file with base roots"

import uvicorn
from fastapi import FastAPI

from src.products.routers import category_router, product_router


app = FastAPI(
    title="FastApi Products",
    description="Simple pet project",
    docs_url="/"
)


app.include_router(category_router)
app.include_router(product_router)


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="127.0.0.1",
        port=8000
    )
