from typing import Final

from starlette.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp


def _construct_origins() -> list[str]:
    allowed_localhost_ports: Final = [80, 3000, 3001]
    allowed_localhost_domains: Final = ["localhost", "127.0.0.1"]
    allowed_localhost_protocols: Final = ["http", "https"]
    origins = [
        f"{protocol}://{domain}:{port}"
        for protocol in allowed_localhost_protocols
        for domain in allowed_localhost_domains
        for port in allowed_localhost_ports
    ]

    # there's no need for ports here since the api is behind a proxy
    allowed_public_domains = [
        "https://dev.thehub-aubg.com",
        "https://thehub-aubg.com",
    ]

    origins.extend(allowed_public_domains)

    return origins


def cors_middleware_factory(app: ASGIApp) -> CORSMiddleware:
    return CORSMiddleware(
        app=app,
        allow_origins=_construct_origins(),
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
