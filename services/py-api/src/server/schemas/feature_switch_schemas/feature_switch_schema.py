from typing import Any, Dict
from pydantic import BaseModel

class FeatureSwitch(BaseModel):
    state: bool
    name: str

    def dump_as_json(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "state": self.state
        }