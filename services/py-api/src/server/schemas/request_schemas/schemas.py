
from pydantic import EmailStr, BaseModel


class ParticipantRequestBody(BaseModel):
    name: str
    email: EmailStr
    team_name: str
    is_admin: bool


# class CreateParticipantInTeamInputData(ParticipantRequestBody):
#     """This is used as an intermediary when creating a participant and a team in a transaction in order to get
#      the team_id from the created team and pass it as input data to the `create` func in the ParticipantRepository"""
#     team_id: Optional[ObjectId]
#
#     class Config:
#         arbitrary_types_allowed = True
