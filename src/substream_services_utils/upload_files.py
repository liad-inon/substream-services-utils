import io
from typing import BinaryIO

from fastapi import UploadFile


async def load_upload_files(upload_files: list[UploadFile]) -> list[BinaryIO]:
    return [
        await load_upload_file(file) for file in upload_files
    ]


async def load_upload_file(upload_file: UploadFile) -> BinaryIO:
    file_contents = await upload_file.read()

    return io.BytesIO(file_contents)
