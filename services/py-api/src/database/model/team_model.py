from src.database.model.base_model import Base


class Team(Base):
    name: str  # unique
    is_verified: bool = False
