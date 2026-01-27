from abc import ABC
from typing import Any
from starlette import status
from pymongo.errors import DuplicateKeyError

ERROR_MAPPING: dict[type[BaseException], tuple[str, int]] = {}
"""Maps custom errors to their representation (message, status_code), dynamically populated once a subclass of
CustomError is created (not instantiated)"""


class CustomError(ABC, BaseException):
    """Base class for all custom errors. Inheritors should override ``message`` and ``status_code``"""

    message: str
    status_code: int

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        This method is called when a class is subclassed.
        The default implementation does nothing. It may be overridden to extend subclasses.
        """
        super().__init_subclass__(**kwargs)

        # Add to the error mapping
        ERROR_MAPPING[cls] = (cls.message, cls.status_code)


class DuplicateEmailError(CustomError, DuplicateKeyError):
    message = "Participant with this email already exists"
    status_code = status.HTTP_409_CONFLICT


class DuplicateTeamNameError(CustomError, DuplicateKeyError):
    message = "Team with this name already exists"
    status_code = status.HTTP_409_CONFLICT


class HackathonCapacityExceededError(CustomError):
    """Exception raised when hackathon capacity has been reached."""

    message = "Max hackathon capacity has been reached"
    status_code = status.HTTP_409_CONFLICT


class ParticipantNotFoundError(CustomError):
    """Exception raised when there are no participants that match the query to the database"""

    message = "The specified participant was not found"
    status_code = status.HTTP_404_NOT_FOUND


class EmailRateLimitExceededError(CustomError):
    """Exception raised when the user has exceeded the rate limit for sending emails"""

    # placeholder value to satisfy __init_subclass__, message is overridden in the __init__
    message = ""
    status_code = status.HTTP_429_TOO_MANY_REQUESTS

    def __init__(self, seconds_to_retry_after: int):
        self.message = (
            f"The rate limit for sending emails has been exceeded. Try again after {seconds_to_retry_after} seconds."
        )
        # Overriding the saved cls in the error_mapping when __init_subclass__ was first called
        ERROR_MAPPING[self.__class__] = (self.message, self.status_code)


class ParticipantAlreadyVerifiedError(CustomError):
    """Exception raised when the user has already been verified"""

    message = "You have already been verified"
    status_code = status.HTTP_400_BAD_REQUEST


class TeamNotFoundError(CustomError):
    """Exception raised when there are no teams that match the query to the database"""

    message = "The specified team was not found"
    status_code = status.HTTP_404_NOT_FOUND


class TeamCapacityExceededError(CustomError):
    """Exception raised when team capacity has been reached"""

    message = "Max team capacity has been reached"
    status_code = status.HTTP_409_CONFLICT


class TeamNameMissmatchError(CustomError):
    """Exception raised when the ``team_name`` passed in the request body is different from the ``team_name`` in the
    decoded JWT token, when a participant is registering via an invitation link.
    """

    message = "team_name passed in the request body is different from the team_name in the decoded JWT token"
    status_code = status.HTTP_400_BAD_REQUEST


class SponsorNotFoundError(CustomError):
    """Exception raised when the sponsor cannot be found in the database"""

    message = "The specified sponsor was not found"
    status_code = status.HTTP_404_NOT_FOUND


class JwtDecodeSchemaMismatch(CustomError):
    """Exception raised when the decoded token does not match the structure of the defined JWT schema"""

    message = "The decoded token does not match the Jwt schema"
    status_code = status.HTTP_400_BAD_REQUEST


class JwtInvalidSignatureError(CustomError):
    """Exception raised by the Jwt Utility when the token has an invalid signature"""

    message = "The JWT token has invalid signature."
    status_code = status.HTTP_400_BAD_REQUEST


class JwtExpiredSignatureError(CustomError):
    """Exception raised by the Jwt Utility when the token has expired"""

    message = "The JWT token has expired."
    status_code = status.HTTP_400_BAD_REQUEST


class JwtDecodeError(CustomError):
    """Exception raised by the Jwt Utility when the token cannot be decoded"""

    message = "There was a a general error while decoding the JWT token. Checks its format again."
    status_code = status.HTTP_400_BAD_REQUEST


class FeatureSwitchNotFoundError(CustomError):
    message = "The feature switch was not found."
    status_code = status.HTTP_404_NOT_FOUND


class PastEventNotFoundError(CustomError):
    """Exception raised when a past event with the given id does not exist"""

    message = "The specified past event was not found"
    status_code = status.HTTP_404_NOT_FOUND


class ImageCompressionError(Exception):
    """Exception raised when the image compression fails"""

    message = "There was an error when compressing the image"


class FileUploadError(Exception):
    """Exception raised when uploading a file to aws fails"""

    message = "There was an error when uploading the file"
