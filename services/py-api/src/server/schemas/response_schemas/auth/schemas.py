from pydantic import BaseModel


class AccessTokenSuccessfullyIssued(BaseModel):
    """
    Responds upon a successful session refresh
    """

    access_token: str


class AuthTokensSuccessfullyIssued(AccessTokenSuccessfullyIssued):
    """
    Responds upon a successful login for a hub admin, returning their access token and id token
    """

    id_token: str
