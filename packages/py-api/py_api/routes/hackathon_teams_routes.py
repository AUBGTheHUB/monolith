from fastapi import APIRouter
from fastapi.responses import JSONResponse
from py_api.controllers import TeamsController as c
from py_api.models import UpdateTeam

router = APIRouter(prefix="/hackathon/teams")


@router.get("")
def get_all_teams() -> JSONResponse:
    return c.fetch_teams()


@router.get("/count")
def team_count() -> JSONResponse:
    return c.team_count()


@router.get("/{object_id}")
def get_team(object_id: str) -> JSONResponse:
    return c.get_team(object_id)


@router.put("/{object_id}")
def update_team(object_id: str, update_form: UpdateTeam) -> JSONResponse:
    return c.update_team(object_id, update_form)


@router.delete("/{object_id}")
def delete_team(object_id: str) -> JSONResponse:
    return c.delete_team(object_id)
