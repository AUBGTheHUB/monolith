from pymongo.errors import DuplicateKeyError


class DuplicateEmailError(DuplicateKeyError):
    pass


class DuplicateTeamNameError(DuplicateKeyError):
    pass


class HackathonCapacityExceededError(Exception):
    """Exception raised when hackathon capacity has been reached."""


class ParticipantNotFound(Exception):
    """Exception raised when there are no participants that match the query to the database"""


class TeamNotFound(Exception):
    """Exception raised when there are no teams that match the query to the database"""
