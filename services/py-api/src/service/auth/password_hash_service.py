from typing import cast
from bcrypt import checkpw, gensalt, hashpw

SALT_ROUNDS = 20


class PasswordHashService:
    def __init__(self) -> None:
        pass

    def hash_password(self, password_string: str) -> bytes:
        bytes_pass = password_string.encode("utf-8")
        salt = gensalt(SALT_ROUNDS)

        pass_hash: bytes = hashpw(bytes_pass, salt)
        return pass_hash

    def check_password(self, actual_password: str, password_attempt: str) -> bool:
        attempt_bytes = password_attempt.encode("utf-8")
        actual_bytes = actual_password.encode("utf-8")

        return cast(bool, checkpw(password=attempt_bytes, hashed_password=actual_bytes))
