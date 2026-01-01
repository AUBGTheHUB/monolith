"""Here we store functions made to be passed as arguments to the route dependencies. These acts as a middleware but on
route level instead of an application level, and get executed first before the request is handled.

For more info: https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/
"""

from os import environ
from typing import Annotated

from bson import ObjectId
from fastapi import Header, HTTPException, Path
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


def is_auth(authorization: Annotated[str, Header()]) -> None:
    # This follows the dependency pattern that is provided to us by FastAPI
    # You can read more about it here:
    # https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/
    # I have exported this function on a separate dependencies file likes suggested in:
    # https://fastapi.tiangolo.com/tutorial/bigger-applications/#another-module-with-apirouter
    # TODO: When the admin panel is implemented, the secret auth toke env variable should be removed as tokens
    #  will be automatically rotated
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
    fs_repo: FeatureSwitchRepository = request.app.state.fs_repo

    result = await fs_repo.get_feature_switch(REG_ALL_PARTICIPANTS_SWITCH)
    if is_err(result):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

    if result.ok_value.state is False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Registration is closed")


# ===============================
# Path Operation Decorators end
# ===============================
