from pydantic import BaseModel


class AdminTokens(BaseModel):
    id_token: str
    access_token: str
    refresh_token: str
