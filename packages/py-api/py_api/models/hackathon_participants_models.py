from pydantic import BaseModel


class NewParticipant(BaseModel):
    first_name: str
    last_name: str
    email: str
    tshirt_size: str
