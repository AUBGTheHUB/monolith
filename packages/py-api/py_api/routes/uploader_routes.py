from typing import Annotated, Any, Dict

from fastapi import APIRouter, Form, UploadFile
from py_api.controllers import UploaderController as c

router = APIRouter(prefix="/uploader")


@router.get("")
async def get_objects() -> Dict[str, Any]:
    return c.dump_objects()


@router.post("")
async def upload_object(file: UploadFile, filename: Annotated[str, Form()]) -> Dict[str, Any]:
    return c.upload_object(file, filename)


@router.delete("/{image_url}")
async def delete_object(image_url) -> Dict[str, Any]:  # type: ignore
    return c.delete_object(image_url)
