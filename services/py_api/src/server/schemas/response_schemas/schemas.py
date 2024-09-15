from pydantic import BaseModel


class ErrResponse(BaseModel):
    error: str


class PongResponse(BaseModel):
    message: str
