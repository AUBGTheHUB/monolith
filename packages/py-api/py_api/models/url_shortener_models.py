from typing import Any, Dict

from pydantic import AnyHttpUrl, BaseModel
from pydantic_core import Url


class ShortenedURL(BaseModel):
    endpoint: str
    url: AnyHttpUrl

    # model_dump will return the following dict
    # {"endpoint": "something", "url": Url("https://something.com")}
    # which is not serializable

    # def model_dump(self):
    #     return {
    #         x: y if not isinstance(y, Url) else str(y)
    #         for x, y in super().model_dump().items()
    #     }

    # both methods perform relatively the same
    # second one is easier to read.
    # the above one can be extracted as a utility function

    def model_dump(self) -> Dict[str, str]:
        dumped_model: Dict[str, Any] = super().model_dump()
        dumped_model["url"] = str(dumped_model["url"])
        return dumped_model
