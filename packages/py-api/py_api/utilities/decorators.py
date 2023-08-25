from fastapi import APIRouter, FastAPI


def bind_router(router: FastAPI):  # type: ignore
    def wrapper(func):  # type: ignore
        def inner_wrapper(*args: APIRouter, **kwargs):  # type: ignore
            result = func(*args, **kwargs)
            args[0].include_router(router)
            return result
        return inner_wrapper
    return wrapper
