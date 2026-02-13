from typing import Any

from pydantic import BaseModel, field_serializer, ConfigDict

from src.database.model.admin.hub_admin_model import HubAdmin


class HubMemberSuccessfullyRegistered(BaseModel):
    # We need this to skip validation during schema generation. Otherwise, we get  Unable to generate pydantic-core
    # schema for <class 'bson.objectid.ObjectId'>
    model_config = ConfigDict(arbitrary_types_allowed=True)

    hub_admin: HubAdmin

    @field_serializer("hub_admin")
    def serialize_hub_admin(self, hub_admin: HubAdmin) -> dict[str, Any]:
        return hub_admin.dump_as_json()


class AccessTokenSuccessfullyIssued(BaseModel):
    """
    Responds upon either a successful login for a hub admin, or successfully refreshing their session
    """

    access_token: str
