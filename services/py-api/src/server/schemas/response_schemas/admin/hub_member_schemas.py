from typing import Any, List

from pydantic import BaseModel, ConfigDict, field_serializer

from src.database.model.admin.hub_member_model import HubMember


class HubMemberResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    hub_member: HubMember

    @field_serializer("hub_member")
    def serialize_hub_member(self, hub_member: HubMember) -> dict[str, Any]:
        return hub_member.dump_as_json()


class HubMembersListResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    members: List[HubMember]

    @field_serializer("members")
    def serialize_hub_members(self, hub_members: list[HubMember]) -> list[dict[str, Any]]:
        return [hub_member.dump_as_json() for hub_member in hub_members]
