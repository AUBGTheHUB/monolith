from src.database.repository.admin.hub_members_repository import HubMembersRepository


# TODO IMPLEMENT
# NOTE REPO might change here implement as you find suitable
class AuthenticationService:
    def __init__(self, repo: HubMembersRepository):
        self._repo = repo
