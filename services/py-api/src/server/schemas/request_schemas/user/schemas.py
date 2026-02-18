from pydantic import BaseModel, Field
from src.database.model.admin.hub_admin_model import AssignableRole


class UserRoleChangeRequest(BaseModel):
    role: AssignableRole = Field(..., description="The new security role to assign to the admin")
