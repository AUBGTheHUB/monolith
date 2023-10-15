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


@router.delete("/{image_name:path}")
async def delete_object(image_name: str) -> Dict[str, Any]:
    return c.delete_object_by_filename(image_name)
