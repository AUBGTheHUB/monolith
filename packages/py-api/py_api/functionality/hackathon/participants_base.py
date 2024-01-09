from py_api.database.initialize import participants_col, t_col


class ParticipantsFunctionality:
    @classmethod
    def check_if_email_exists(cls, email: str) -> bool:
        if participants_col.find_one(filter={"email": email}):
            return True

        return False
