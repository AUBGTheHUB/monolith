from typing import Mapping, Any

from pydantic import BaseModel, ConfigDict, field_serializer
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse

from src.database.model.feature_switch_model import FeatureSwitch


class Response(JSONResponse):
    """A thin wrapper over the Starlette JSONResponse class. This wrapper allows us to pass Response models, which are
    automatically serialized to JSON under the hood.

    For more info: https://fastapi.tiangolo.com/tutorial/response-model/
    """

    def __init__(
        self,
        response_model: BaseModel,
        status_code: int,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ):
        super().__init__(
            content=response_model.model_dump(),
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )
        self.response_model = response_model


class ErrResponse(BaseModel):
    error: str


class PongResponse(BaseModel):
    message: str


class FeatureSwitchResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    feature: FeatureSwitch

    @field_serializer("feature")
    def serialize_feature(self, feature: FeatureSwitch) -> dict[str, Any]:
        return feature.dump_as_json()


class AllFeatureSwitchesResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    features: list[FeatureSwitch]

    @field_serializer("features")
    def serialize_features(self, features: list[FeatureSwitch]) -> list[dict[str, Any]]:
        return [feature.dump_as_json() for feature in features]

