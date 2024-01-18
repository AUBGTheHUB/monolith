from typing import Optional

from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse
from py_api.controllers import ParticipantsController as c
from py_api.models import NewParticipant, UpdateParticipant

router = APIRouter(prefix="/hackathon/participants")

# ? Why are all these using only object id for fetching participants when you have emails defined as unique values


@router.get("")
async def get_participants() -> JSONResponse:
    return c.get_all_participants()


@router.get("/{object_id}")
async def get_participant(object_id: str) -> JSONResponse:
    return c.get_specified_participant(object_id)


@router.put("/{object_id}")
async def update_participant(object_id: str, participant_form: UpdateParticipant) -> JSONResponse:
    return c.update_participant(object_id, participant_form)


@router.post("")
async def add_participant(update_form: NewParticipant, token: Optional[str] = None) -> JSONResponse:
    return await c.add_participant(update_form, token)


@router.delete("/{object_id}")
async def delete_participant(object_id: str) -> JSONResponse:
    return c.delete_participant(object_id)
