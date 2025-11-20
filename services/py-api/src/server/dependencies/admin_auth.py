from fastapi import Depends

# Placeholder dependency for admin authentication.


def require_admin(_: str | None = Depends(lambda: None)) -> None:
    """Temporary stub. Replace lambda with token extraction & validation.

    For now this lets requests pass. Change to raise 401/403 when wiring real auth.
    """
    return None
