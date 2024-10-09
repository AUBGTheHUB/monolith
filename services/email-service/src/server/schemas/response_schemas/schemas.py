from pydantic import BaseModel


class ErrResponse(BaseModel):
    error: str


class EmailSentResponse(BaseModel):
    message: str


class PongResponse(BaseModel):
    message: str
