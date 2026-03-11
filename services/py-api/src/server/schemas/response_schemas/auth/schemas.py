from pydantic import BaseModel


class AuthTokensSuccessfullyIssued(BaseModel):
    """
    Responds upon a successful login for a hub admin, returning their access token and id token
    """

    id_token: str
    access_token: str
