from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException



class DuplicateEmailError(DuplicateKeyError):
    pass


class DuplicateTeamNameError(DuplicateKeyError):
    pass

class CapacityExceededError(HTTPException):
    """Exception raised when hackathon capacity has been reached."""
    def __init__(self):
        super().__init__(status_code=409, detail="The hackathon capacity has been reached.")