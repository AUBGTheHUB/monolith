from json import loads
from re import escape, search
from typing import Any, Callable, Dict, List, Self


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
