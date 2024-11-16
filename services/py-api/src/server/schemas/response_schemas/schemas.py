from pydantic import BaseModel

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team


class ErrResponse(BaseModel):
    error: str


class PongResponse(BaseModel):
    message: str


class AdminParticipantRegisteredResponse(BaseModel):
    participant: Participant
    team: Team