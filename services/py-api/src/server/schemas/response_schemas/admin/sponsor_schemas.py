from typing import Any

from pydantic import BaseModel, ConfigDict, field_serializer

from src.database.model.admin.sponsor_model import Sponsor


class SponsorResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sponsor: Sponsor

    @field_serializer("sponsor")
    def serialize_sponsor(self, sponsor: Sponsor) -> dict[str, Any]:
        return sponsor.dump_as_json()
