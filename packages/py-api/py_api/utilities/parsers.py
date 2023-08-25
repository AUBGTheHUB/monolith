from json import loads
from typing import Any, Callable, Dict


async def parse_request_body(body: Callable[..., bytes]) -> Dict[Any, Any]:
    """ Only works for fastapi.requests.Request.body callables """
    parsed_body: Dict[Any, Any] = loads(await body())
    return parsed_body
