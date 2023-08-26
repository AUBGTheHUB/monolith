from pydantic import BaseModel


class FeatureSwitch(BaseModel):
    switch_id: str
    is_enabled: bool
