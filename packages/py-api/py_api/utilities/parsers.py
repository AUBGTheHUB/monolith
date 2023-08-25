from json import loads
from typing import Any, Callable, Coroutine, Dict


async def parse_request_body(body: Callable[..., bytes]) -> Dict[Any, Any]:
    parsed_body: Dict[Any, Any] = loads(await body())
    return parsed_body
