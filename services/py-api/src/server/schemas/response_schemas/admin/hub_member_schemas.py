from typing import Any

from pydantic import BaseModel, ConfigDict, field_serializer

from src.database.model.admin.hub_member_model import HubMember


class HubMemberResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    hub_member: HubMember

    @field_serializer("hub_member")
    def serialize_hub_member(self, hub_member: HubMember) -> dict[str, Any]:
        return hub_member.dump_as_json()
