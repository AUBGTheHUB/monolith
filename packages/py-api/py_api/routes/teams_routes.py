from typing import Any, Dict

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from py_api.controllers import TeamsController as c

router = APIRouter(prefix="/teams")


@router.get("")
def get_all_teams() -> JSONResponse:
    return c.fetch_teams()


@router.get("/{objectID}")
def get_team(objectID: str) -> JSONResponse:
    return c.get_team(objectID)


# @router.put("/{objectID}")
# def update_team(objectID: str) -> JSONResponse:
#     return c.update_team(objectID)


@router.delete("/{objectID}")
def delete_team(objectID: str) -> JSONResponse:
    return c.delete_team(objectID)


# @router.get("/count/{objectID}")
# def team_count(objectID: str) -> JSONResponse:
#     return c.team_count(objectID)
