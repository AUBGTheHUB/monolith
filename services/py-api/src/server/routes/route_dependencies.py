from os import environ
from typing import Annotated

from bson import ObjectId
from fastapi import Header, HTTPException, Path
from result import is_err
from starlette import status
from starlette.requests import Request
from structlog.stdlib import get_logger

from src.database.repository.feature_switch_repository import FeatureSwitchRepository
from src.service.hackathon.hackathon_service import HackathonService

LOG = get_logger()


def is_auth(authorization: str = Header(..., alias="Authorization")) -> None:
    if not (
        authorization
        and authorization.startswith("Bearer ")
        and authorization[len("Bearer ") :] == environ["SECRET_AUTH_TOKEN"]
    ):
        raise HTTPException(detail="Unauthorized", status_code=401)


def validate_obj_id(object_id: Annotated[str, Path()]) -> None:
    if not ObjectId.is_valid(object_id):
        raise HTTPException(detail="Wrong Object ID format", status_code=400)


async def is_registration_open(request: Request) -> None:
    """Blocks requests when hackathon registration is closed."""
    fs_repo: FeatureSwitchRepository = request.app.state.fs_repo

    result = await fs_repo.get_feature_switch(HackathonService.REG_ALL_PARTICIPANTS_SWITCH)
    if is_err(result):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

    if result.ok_value.state is False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Registration is closed")
