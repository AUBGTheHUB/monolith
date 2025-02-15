"""Here we create FastAPI dependencies using the ``fastapi.Depends`` func. These custom dependencies are injected into
one another, forming a so-called Dependency Graph. This graph is traversed and resolved using FastAPI's internal
Dependency Injection system.

The routes are the entrypoint of incoming requests. For separation of concerns these requests are passed to HTTP
handlers, which are injected into the routes via FastAPI. After that, FastAPI traverses the Dependency graph, resolving
and injecting dependencies along the way. (Handlers have dependencies and these dependencies have their own dependencies
and so on...)

A linear representation of this graph looks something like this:

                          Repositories -> DbManagers -> DbClients
                         /
Routes -> Handlers -> Services -> OtherServices -> OtherComponents
                         \
                          MailServices ->  MailClients


To create a FastAPI dependency we could make use of our own "provider" functions defined alongside every component of
our system.

Note that some providers expect as args automatically injected instances by FastAPI using ``fastapi.Depends``, meaning
we could pass them directly some of the created FastAPI dependencies below"""

from os import environ
from typing import Annotated

from bson import ObjectId
from fastapi import HTTPException, Header, Path

from src.environment import is_prod_env

# ======================================
# Path operation decorators creation start
# ======================================


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


# ======================================
# Path operation decorators creation end
# ======================================
