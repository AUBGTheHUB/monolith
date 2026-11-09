from httpx import AsyncClient


def get_http_client() -> AsyncClient:
    return AsyncClient()
