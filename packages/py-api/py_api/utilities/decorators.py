from typing import Any, Callable, TypeVar, cast

FuncT = TypeVar('FuncT', bound=Callable[..., Any])


def handle_exception(func: FuncT) -> FuncT:
    def wrapper(*arg, **kwargs):  # type: ignore
        request = arg[0]
        try:
            response = func(*arg, **kwargs)
            return response
        except Exception as e:
            e.handle_body = request.body  # type: ignore
            raise e

    return cast(FuncT, wrapper)
