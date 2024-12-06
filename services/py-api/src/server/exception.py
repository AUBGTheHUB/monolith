from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException



class DuplicateEmailError(DuplicateKeyError):
    pass


class DuplicateTeamNameError(DuplicateKeyError):
    pass

class HackathonCapacityExceededError(Exception):
    """Exception raised when hackathon capacity has been reached."""
    pass

class TeamCapacityExceededError(Exception):
    """Exception raised when team capacity has been reached."""
    pass