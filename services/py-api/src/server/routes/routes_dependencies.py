"""Here we store functions made to be passed as arguments to the ``fastapi.Depends`` which is used to create special
FastAPI Dependencies passed to the routes like this:

def get_feature_switch_handlers() -> FeatureSwitchHandler:
    return FEATURE_SWITCH_HANDLERS

which is passed to the route like this:

@utility_router.get("/feature-switches/{feature}")
async def get_feature_switch(feature: str, handler: FeatureSwitchHandler = Depends(get_feature_switch_handlers)) -> Response:
    return await handler.handle_feature_switch(feature=feature)

We have to do this because if we passed a provider function directly to ``fastapi.Depends`` like this:

@utility_router.get("/feature-switches/{feature}")
async def get_feature_switch(feature: str, handler: FeatureSwitchHandler = Depends(feature_switch_handlers_provider)) -> Response:
    return await handler.handle_feature_switch(feature=feature)

FastAPI won't be able to resolve the sub-dependencies which are needed in order to create a `FeatureSwitchHandler`
instance, and we will get an error, similar to this one:

"fastapi.exceptions.FastAPIError: Invalid args for response field! Hint: check that
<class 'src.service.feature_switch_service.FeatureSwitchService'> is a valid Pydantic field type"

We get this error, because FastAPI expects the arguments of dependencies to be passed as path/query params, or to use
a PydanticModel for describing these arguments in Swagger.

Call stack (simplified) for the curious ones:
1. https://github.com/fastapi/fastapi/blob/8c9c536c0a277125ca95c0d9ef19e2c6a39d1db8/fastapi/routing.py#L554
2. https://github.com/fastapi/fastapi/blob/8c9c536c0a277125ca95c0d9ef19e2c6a39d1db8/fastapi/dependencies/utils.py#L285
3. https://github.com/fastapi/fastapi/blob/8c9c536c0a277125ca95c0d9ef19e2c6a39d1db8/fastapi/dependencies/utils.py#L488
4. https://github.com/fastapi/fastapi/blob/8c9c536c0a277125ca95c0d9ef19e2c6a39d1db8/fastapi/utils.py#L63

To avoid this we directly pass an already created instance as a Dependency. In this way FastAPI uses it directly
instead of trying to create it and resolve sub-dependencies if any.

For more info: https://fastapi.tiangolo.com/tutorial/dependencies/
"""

from os import environ
from typing import Annotated, cast

from bson import ObjectId
from fastapi import Header, HTTPException, Path, Depends
from starlette import status
from structlog.stdlib import get_logger

from src.dependency_wiring import (
    FEATURE_SWITCH_HANDLERS,
    HACKATHON_MANAGEMENT_HANDLERS,
    PARTICIPANT_HANDLERS,
    VERIFICATION_HANDLERS,
    UTILITY_HANDLERS,
)
from src.server.handlers.feature_switch_handler import FeatureSwitchHandler
from src.server.handlers.hackathon.hackathon_handlers import HackathonManagementHandlers
from src.server.handlers.hackathon.participants_handlers import ParticipantHandlers
from src.server.handlers.hackathon.verification_handlers import VerificationHandlers
from src.server.handlers.utility_hanlders import UtilityHandlers
from src.server.schemas.response_schemas.schemas import FeatureSwitchResponse
from src.service.hackathon.hackathon_service import HackathonService

LOG = get_logger()


# ===============================
# Request Handlers start
# ===============================


def get_feature_switch_handlers() -> FeatureSwitchHandler:
    """This function is designed to be passes to the ``fastapi.Depends`` function which expects a "callable" .
    ``fastapi.Depends`` will automatically inject the already created FeatureSwitchHandler instance into its intended
    consumers (the routes) by calling this function."""
    return FEATURE_SWITCH_HANDLERS


def get_hackathon_management_handlers() -> HackathonManagementHandlers:
    """This function is designed to be passes to the ``fastapi.Depends`` function which expects a "callable" .
    ``fastapi.Depends`` will automatically inject the already created HackathonManagementHandlers instance into its
    intended consumers (the routes) by calling this function."""
    return HACKATHON_MANAGEMENT_HANDLERS


def get_participant_handlers() -> ParticipantHandlers:
    """This function is designed to be passes to the ``fastapi.Depends`` function which expects a "callable" .
    ``fastapi.Depends`` will automatically inject the already created ParticipantHandlers instance into its intended
    consumers (the routes) by calling this function."""
    return PARTICIPANT_HANDLERS


def get_utility_handlers_handlers() -> UtilityHandlers:
    """This function is designed to be passes to the ``fastapi.Depends`` function which expects a "callable" .
    ``fastapi.Depends`` will automatically inject the already created UtilityHandlers instance into its intended
    consumers (the routes) by calling this function."""
    return UTILITY_HANDLERS


def get_verification_handlers() -> VerificationHandlers:
    """This function is designed to be passes to the ``fastapi.Depends`` function which expects a "callable" .
    ``fastapi.Depends`` will automatically inject the already created VerificationHandlers instance into its intended
    consumers (the routes) by calling this function."""
    return VERIFICATION_HANDLERS


# ===============================
# Request Handlers end
# ===============================


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


async def registration_open(fs_handler: FeatureSwitchHandler = Depends(get_feature_switch_handlers)) -> None:
    resp = await fs_handler.get_feature_switch(feature=HackathonService.REG_ALL_PARTICIPANTS_SWITCH)

    if resp.status_code != 200:
        LOG.error(
            "Error while fetching FS before registration request is accepted",
            feature=HackathonService.REG_ALL_PARTICIPANTS_SWITCH,
            status_code=resp.status_code,
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occured")

    resp_data = cast(FeatureSwitchResponse, resp.response_model)
    if resp_data.feature.state is False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Registration is closed")


# ===============================
# Path Operation Decorators end
# ===============================
