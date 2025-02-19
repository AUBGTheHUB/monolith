"""Here we store functions made to be passed as arguments to the ``fastapi.Depends`` which is used to create special
FastAPI Dependencies passed to the routes.

For more info: https://fastapi.tiangolo.com/tutorial/dependencies/
"""

from os import environ
from typing import Annotated

from bson import ObjectId
from fastapi import Header, HTTPException, Path

from src.dependency_wiring import (
    FEATURE_SWITCH_HANDLERS,
    HACKATHON_MANAGEMENT_HANDLERS,
    PARTICIPANT_HANDLERS,
    VERIFICATION_HANDLERS,
    UTILITY_HANDLERS,
)
from src.server.handlers.feature_switch_handler import FeatureSwitchHandler
from src.server.handlers.hackathon_handlers import HackathonManagementHandlers
from src.server.handlers.participants_handlers import ParticipantHandlers
from src.server.handlers.utility_hanlders import UtilityHandlers
from src.server.handlers.verification_handlers import VerificationHandlers


# ===============================
# Request Handlers start
# ===============================
def get_feature_switch_handlers() -> FeatureSwitchHandler:
    """This function is designed to be passes to the ``fastapi.Depends`` function which expects a "callable" .
    ``fastapi.Depends`` will automatically inject the FeatureSwitchHandler instance into its intended consumers (routes)
     by calling this function."""
    return FEATURE_SWITCH_HANDLERS


def get_hackathon_management_handlers() -> HackathonManagementHandlers:
    """This function is designed to be passes to the ``fastapi.Depends`` function which expects a "callable" .
    ``fastapi.Depends`` will automatically inject the HackathonManagementHandlers instance into its intended consumers
    (routes) by calling this function."""
    return HACKATHON_MANAGEMENT_HANDLERS


def get_participant_handlers() -> ParticipantHandlers:
    """This function is designed to be passes to the ``fastapi.Depends`` function which expects a "callable" .
    ``fastapi.Depends`` will automatically inject the ParticipantHandlers instance into its intended consumers (routes)
    by calling this function."""
    return PARTICIPANT_HANDLERS


def get_utility_handlers_handlers() -> UtilityHandlers:
    """This function is designed to be passes to the ``fastapi.Depends`` function which expects a "callable" .
    ``fastapi.Depends`` will automatically inject the UtilityHandlers instance into its intended consumers (routes)
    by calling this function."""
    return UTILITY_HANDLERS


def get_verification_handlers() -> VerificationHandlers:
    """This function is designed to be passes to the ``fastapi.Depends`` function which expects a "callable" .
    ``fastapi.Depends`` will automatically inject the VerificationHandlers instance into its intended consumers (routes)
    by calling this function."""
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
    if environ["ENV"] != "PROD":
        if not (
            authorization
            and authorization.startswith("Bearer ")
            and authorization[len("Bearer ") :] == environ["SECRET_AUTH_TOKEN"]
        ):
            raise HTTPException(detail="Unauthorized", status_code=401)
    else:
        # TODO: Implement JWT Bearer token authorization logic if we decide on an admin panel.
        #  For now every effort to access protected routes in a PROD env will not be authorized!
        raise HTTPException(detail="Unauthorized", status_code=401)


def validate_obj_id(object_id: Annotated[str, Path()]) -> None:
    if not ObjectId.is_valid(object_id):
        raise HTTPException(detail="Wrong Object ID format", status_code=400)


# TODO: Since Alex has created more specific feature switches this logic shall be changed
# async def registration_open(service: FeatureSwitchService = Depends(_fs_service)) -> None:
#
#     result = await service.check_feature_switch(feature=REGISTRATION_FEATURE_SWITCH)
#
#     if is_err(result):
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occured")
#
#     if result.ok_value.state is False:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Registration is closed")


# ===============================
# Path Operation Decorators end
# ===============================
