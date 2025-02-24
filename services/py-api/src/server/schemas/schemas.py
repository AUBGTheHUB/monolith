from typing import TypedDict

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team


class RandomTeam(TypedDict):
    team: Team
    participants: list[Participant]
