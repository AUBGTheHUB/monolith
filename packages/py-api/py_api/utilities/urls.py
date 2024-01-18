from fastapi import Request


def get_hostname_with_protocol(request: Request) -> str:
    return f"{request.url.scheme}://{request.base_url.hostname}{f':{request.base_url.port}' if request.base_url.port else ''}"
