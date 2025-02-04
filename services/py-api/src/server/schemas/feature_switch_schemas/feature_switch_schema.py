from pydantic import BaseModel

class FeatureSwitch(BaseModel):
    feature: str
    state: bool