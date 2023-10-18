from typing import Any, Dict

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from py_api.controllers import PartcipantsController as c
from py_api.models import RandomParticipant

router = APIRouter(prefix="/hackathon/participants")


@router.get("")
async def get_participants() -> JSONResponse:
    return c.get_all_participants()


@router.get("/{object_id}")
async def get_participant(object_id: str) -> JSONResponse:
    return c.get_specified_participant(object_id)


@router.put("/{object_id}")
async def upsert_participant(object_id: str, participant_form: RandomParticipant) -> JSONResponse:
    return c.upsert_participant(object_id, participant_form)


@router.post("")
async def add_participant(participant_form: RandomParticipant) -> JSONResponse:
    return c.add_participant(participant_form)


@router.delete("/{object_id}")
async def delete_participant(object_id: str) -> JSONResponse:
    return c.delete_participant(object_id)
