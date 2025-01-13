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
    TeamNotFoundError,
)
from starlette import status

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

ERROR_MAPPING = {
            DuplicateEmailError: ("Participant with this email already exists", status.HTTP_409_CONFLICT),
            DuplicateTeamNameError: ("Team with this name already exists", status.HTTP_409_CONFLICT),
            HackathonCapacityExceededError: ("Max hackathon capacity has been reached", status.HTTP_409_CONFLICT),
            TeamCapacityExceededError: ("Max team capacity has been reached", status.HTTP_409_CONFLICT),
            TeamNotFoundError: ("The specified team was not found", status.HTTP_404_NOT_FOUND),
            TeamNameMissmatchError: (
                "team_name passed in the request body is different from the team_name in the" "decoded JWT token",
                status.HTTP_400_BAD_REQUEST,
            ),
        }

type ParticipantRegistrationOkValue = Tuple[Participant, Team | None]

type DispatchResult = Awaitable[Result[ParticipantRegistrationOkValue, ParticipantRegistrationErrors]]
