

from logging import getLogger
from typing import Final, List

logger = getLogger("CORS")


def construct_origins() -> List[str]:
    ALLOWED_LOCALHOST_PORTS: Final = [3000, 3001]
    ALLOWED_LOCALHOST_DOMAINS: Final = ["localhost", "127.0.0.1"]
    ALLOWED_LOCALHOST_PROTOCOLS: Final = ["http", "https"]
    origins = [f"{protocol}://{domain}:{port}" for protocol in ALLOWED_LOCALHOST_PROTOCOLS for domain in ALLOWED_LOCALHOST_DOMAINS for port in ALLOWED_LOCALHOST_PORTS]

    # there's no need for ports here since the api is behind a proxy
    ALLOWED_PUBLIC_DOMAINS = [
        "https://dev.thehub-aubg.com",
        "https://thehub-aubg.com",
    ]

    origins.extend(ALLOWED_PUBLIC_DOMAINS)

    return origins
