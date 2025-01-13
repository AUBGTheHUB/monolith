from abc import ABC
from typing import Dict, Tuple, Type

from pymongo.errors import DuplicateKeyError

ERROR_MAPPING: Dict[Type[BaseException], Tuple[str, int]] = {}
"""Maps custom errors to their representation (message, status_code), dynamically populated once a subclass of
CustomError is instantiated."""


class CustomError(ABC, BaseException):
    """Base class for all custom errors. Inheritors should override ``message`` and ``status_code``"""

    message: str
    status_code: int

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # Add to the error mapping
        ERROR_MAPPING[cls] = (cls.message, cls.status_code)


class DuplicateEmailError(CustomError, DuplicateKeyError):
    message = "Participant with this email already exists"
    status_code = 409


class DuplicateTeamNameError(CustomError, DuplicateKeyError):
    message = "Participant with this email already exists"
    status_code = 409


class HackathonCapacityExceededError(CustomError):
    """Exception raised when hackathon capacity has been reached."""

    message = "Participant with this email already exists"
    status_code = 409


class ParticipantNotFoundError(CustomError):
    """Exception raised when there are no participants that match the query to the database"""

    message = "Participant with this email already exists"
    status_code = 409


class TeamNotFoundError(CustomError):
    """Exception raised when there are no teams that match the query to the database"""

    message = "Participant with this email already exists"
    status_code = 409


class TeamCapacityExceededError(CustomError):
    """Exception raised when team capacity has been reached"""

    message = "Participant with this email already exists"
    status_code = 409


class TeamNameMissmatchError(CustomError):
    """Exception raised when the ``team_name`` passed in the request body is different from the ``team_name`` in the
    decoded JWT token, when a participant is registering via an invitation link.
    """

    message = "Participant with this email already exists"
    status_code = 409


class JwtDecodeSchemaMismatch(CustomError):
    """Exception raised when the decoded token does not match the structure of the defined JWT schema"""

    message = "Participant with this email already exists"
    status_code = 409


# ERROR_MAPPING = {
#     DuplicateEmailError: ("", status.HTTP_409_CONFLICT),
#     DuplicateTeamNameError: ("Team with this name already exists", status.HTTP_409_CONFLICT),
#     HackathonCapacityExceededError: ("Max hackathon capacity has been reached", status.HTTP_409_CONFLICT),
#     TeamCapacityExceededError: ("Max team capacity has been reached", status.HTTP_409_CONFLICT),
#     TeamNotFoundError: ("The specified team was not found", status.HTTP_404_NOT_FOUND),
#     TeamNameMissmatchError: (
#         "team_name passed in the request body is different from the team_name in the" "decoded JWT token",
#         status.HTTP_400_BAD_REQUEST,
#     ),
# }
