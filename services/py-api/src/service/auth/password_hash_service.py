from asyncio import to_thread
from bcrypt import checkpw, gensalt, hashpw

SALT_ROUNDS = 12


class PasswordHashService:
    def __init__(self) -> None:
        pass

    async def hash_password(self, password_string: str) -> bytes:
        bytes_pass = password_string.encode("utf-8")
        salt = gensalt(SALT_ROUNDS)

        hashed_password: bytes = await to_thread(hashpw, bytes_pass, salt=salt)
        return hashed_password

    async def check_password(self, actual_password: str, password_attempt: str) -> bool:
        attempt_bytes = password_attempt.encode("utf-8")
        actual_bytes = actual_password.encode("utf-8")

        is_valid: bool = await to_thread(checkpw, attempt_bytes, actual_bytes)
        return is_valid
