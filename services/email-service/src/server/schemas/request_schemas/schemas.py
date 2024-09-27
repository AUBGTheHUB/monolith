from pydantic import BaseModel, EmailStr


class RequestBody(BaseModel):
    subject: str
    receiver: EmailStr
    body: str
