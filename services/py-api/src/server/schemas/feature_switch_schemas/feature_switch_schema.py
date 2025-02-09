from pydantic import BaseModel

class FeatureSwitch(BaseModel):
    state: bool
    name: str