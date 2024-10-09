from pydantic import EmailStr

from src.database.model.base_model import Base


class Participant(Base):
    name: str
    email: EmailStr
    is_admin: bool
    email_verified: bool = False
