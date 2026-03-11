from typing import Any, List
from pydantic import BaseModel, ConfigDict, field_serializer
from src.database.model.admin.hub_admin_model import HubAdmin


class HubAdminsListResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    admins: List[HubAdmin]

    @field_serializer("admins")
    def serialize_hub_members(self, hub_admins: list[HubAdmin]) -> list[dict[str, Any]]:
        return [hub_admin.dump_basic_information() for hub_admin in hub_admins]
