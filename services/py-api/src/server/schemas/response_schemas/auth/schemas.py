from pydantic import BaseModel


class AccessTokenSuccessfullyIssued(BaseModel):
    """
    Responds upon either a successful login for a hub admin, or successfully refreshing their session
    """

    access_token: str
