from json import loads
from typing import Any, Callable, Coroutine, Dict


async def parse_request_body(body: Callable[..., bytes]) -> Dict[Any, Any]:
    parsed_body: Dict[Any, Any] = loads(await body())
    raise Exception
    return parsed_body
