import secrets
import string

CODE_ALPHABET = string.ascii_letters + string.digits


class TournamentCodeService:
    def __init__(self) -> None:
        pass

    # will determine a better way later
    def generate_team_code(self) -> str:
        return "".join(secrets.choice(CODE_ALPHABET) for _ in range(8))
