"module for utils"

import base64

import aiofiles

from .database import engine, Base

async def create_tables() -> None:
    "Coroutine creates tables using Base metadata"
    async with engine.begin() as connection:

        await connection.run_sync(Base.metadata.create_all, checkfirst=True)

    await engine.dispose()


async def download_image(bytes_data: bytes, file_name: str) -> str:
    "Coroutine downloads image and returns file path"
    file_path = f"media/images/{file_name}"
    async with aiofiles.open(file=file_path, mode="wb") as file:
        await file.write(bytes_data)

    return file_path

#DOESN'T DECODE WELL. IMAGE STILL BAD
async def download_image_base64(bytes_data: bytes, file_name: str) -> str:
    "Coroutine download image in base64 encoding and returns file path"
    file_path = f"media/images/{file_name}"
    async with aiofiles.open(file=file_path, mode="wb") as file:
        await file.write(base64.encodebytes(bytes_data))

    return file_path
