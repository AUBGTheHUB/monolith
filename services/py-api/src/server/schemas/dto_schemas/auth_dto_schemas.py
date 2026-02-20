from pydantic import BaseModel


class AuthTokens(BaseModel):
    access_token: str
    refresh_token: str


class AdminTokens(AuthTokens):
    id_token: str
