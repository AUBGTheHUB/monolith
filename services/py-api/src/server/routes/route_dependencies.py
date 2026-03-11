"""Here we store functions made to be passed as arguments to the route dependencies. These acts as a middleware but on
route level instead of an application level, and get executed first before the request is handled.

For more info: https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/
"""

from typing import Annotated

from bson import ObjectId
from fastapi import HTTPException, Path
from result import is_err
from starlette import status
from starlette.requests import Request
from structlog.stdlib import get_logger

from src.database.repository.feature_switch_repository import FeatureSwitchRepository
from src.service.feature_switches.feature_switches import REG_ALL_PARTICIPANTS_SWITCH

LOG = get_logger()


# ===============================
# Path Operation Decorators start
# ===============================


def validate_obj_id(object_id: Annotated[str, Path()]) -> None:
    if not ObjectId.is_valid(object_id):
        raise HTTPException(detail="Wrong Object ID format", status_code=400)


async def is_registration_open(request: Request) -> None:
    fs_repo: FeatureSwitchRepository = request.app.state.fs_repo

    result = await fs_repo.get_feature_switch(REG_ALL_PARTICIPANTS_SWITCH)
    if is_err(result):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

    if not result.ok_value.state:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Registration is closed")


# ===============================
# Path Operation Decorators end
# ===============================
