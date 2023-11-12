from json import loads
from re import escape, search
from typing import Any, Callable, Dict

from pydantic import BaseModel


async def parse_request_body(body: Callable[..., bytes]) -> Dict[Any, Any]:
    """ Only works for fastapi.requests.Request.body callables """
    parsed_body: Dict[Any, Any] = loads(await body())
    return parsed_body


def eval_bool(bl: str | bool) -> bool:
    if type(bl) == bool:
        return bl
    else:
        bl = bl.strip().lower()
        if bl == "true":
            return True
        else:
            return False


def has_prohibited_characters(input_string: str, prohibited_pattern: str) -> bool:
    prohibited_pattern = f"[{escape(prohibited_pattern)}]"
    return bool(search(prohibited_pattern, input_string))


class AttrDict(dict[Any, Any]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def filter_none_values(document: BaseModel) -> Dict[str, Any]:
    # Creates a dictionary for the specific form
    form_dump = document.model_dump()
    fields_to_be_updated = {}

    # It pushes the fields whose value is not null to the empty dictionary
    for key, value in form_dump.items():
        if value:
            fields_to_be_updated[key] = value

    return fields_to_be_updated
