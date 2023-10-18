from pydantic import BaseModel


class RandomParticipant(BaseModel):
    first_name: str
    last_name: str
    email: str
    Tshirt_size: str
