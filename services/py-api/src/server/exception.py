from pymongo.errors import DuplicateKeyError


class DuplicateEmail(DuplicateKeyError):
    pass


class DuplicateTeamName(DuplicateKeyError):
    pass
