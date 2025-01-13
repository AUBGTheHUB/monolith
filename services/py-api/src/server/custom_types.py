from typing import Awaitable, Tuple, Union

from result import Result

from src.database.model.participant_model import Participant
from src.database.model.team_model import Team
from src.server.exception import (
    DuplicateEmailError,
    DuplicateTeamNameError,
    HackathonCapacityExceededError,
    TeamCapacityExceededError,
    TeamNameMissmatchError,
)

# https://docs.python.org/3/reference/simple_stmts.html#the-type-statement

type ParticipantRegistrationErrors = Union[
    DuplicateEmailError,
    DuplicateTeamNameError,
    TeamCapacityExceededError,
    TeamNameMissmatchError,
    HackathonCapacityExceededError,
    str,
    Exception,
]

type ParticipantParticipantRegistrationOkValue = Tuple[Participant, Team]

type DispatchResult = Awaitable[Result[ParticipantParticipantRegistrationOkValue, ParticipantRegistrationErrors]]
