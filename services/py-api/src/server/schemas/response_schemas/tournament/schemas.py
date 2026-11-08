from typing import Any

from pydantic import BaseModel, ConfigDict, field_serializer

from src.database.model.tournament.group_model import Group


class GroupResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    group: Group

    @field_serializer("group")
    def serialize_group(self, group: Group) -> dict[str, Any]:
        return group.dump_as_json()


class AllGroupsResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    groups: list[Group]

    @field_serializer("groups")
    def serialize_groups(self, groups: list[Group]) -> list[dict[str, Any]]:
        return [group.dump_as_json() for group in groups]
