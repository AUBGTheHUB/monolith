import secrets

CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


class TournamentCodeService:
    def __init__(self) -> None:
        pass

    # will determine a better way later
    def generate_team_code(self) -> str:
        return "".join(secrets.choice(CODE_ALPHABET) for _ in range(8))
