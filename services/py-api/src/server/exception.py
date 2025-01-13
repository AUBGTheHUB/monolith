from pymongo.errors import DuplicateKeyError


class DuplicateEmailError(DuplicateKeyError):
    pass


class DuplicateTeamNameError(DuplicateKeyError):
    pass


class HackathonCapacityExceededError(Exception):
    """Exception raised when hackathon capacity has been reached."""


class ParticipantNotFoundError(Exception):
    """Exception raised when there are no participants that match the query to the database"""


class TeamNotFoundError(Exception):
    """Exception raised when there are no teams that match the query to the database"""


class TeamCapacityExceededError(Exception):
    """Exception raised when team capacity has been reached"""


class TeamNameMissmatchError(Exception):
    """Exception raised when the ``team_name`` passed in the request body is different from the ``team_name`` in the
    decoded JWT token, when a participant is registering via an invitation link.
    """
