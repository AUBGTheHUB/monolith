from os import environ
from typing import Annotated

from bson import ObjectId
from fastapi import HTTPException, Header, Path

from src.environment import is_prod_env


def is_auth(authorization: Annotated[str, Header()]) -> None:
    """Path operation decorator verifying if a client is authorized to access a given route"""
    # This follows the dependency pattern that is provided to us by FastAPI
    # You can read more about it here:
    # https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/
    # I have exported this function on a separate dependencies file likes suggested in:
    # https://fastapi.tiangolo.com/tutorial/bigger-applications/#another-module-with-apirouter
    if not is_prod_env():
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
    """Path operation decorator verifying the format of a passed Object ID as path param"""
    if not ObjectId.is_valid(object_id):
        raise HTTPException(detail="Wrong Object ID format", status_code=400)
