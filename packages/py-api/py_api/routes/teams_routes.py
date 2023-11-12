from typing import Any, Dict

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from py_api.controllers import TeamsController as c
from py_api.models import UpdateTeam

router = APIRouter(prefix="/teams")


@router.get("")
def get_all_teams() -> JSONResponse:
    return c.fetch_teams()


@router.get("/count")
def team_count() -> JSONResponse:
    return c.team_count()


@router.get("/{objectID}")
def get_team(objectID: str) -> JSONResponse:
    return c.get_team(objectID)


@router.put("/{objectID}")
def update_team(objectID: str, update_form: UpdateTeam) -> JSONResponse:
    return c.update_team(objectID, update_form)


@router.delete("/{objectID}")
def delete_team(objectID: str) -> JSONResponse:
    return c.delete_team(objectID)
