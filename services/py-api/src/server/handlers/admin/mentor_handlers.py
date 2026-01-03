from src.service.admin.mentors_service import MentorsService


# Mentors Handlers
class MentorsHandlers(BaseException):
    def __init__(self, service: MentorsService) -> None:
        self._service = service

    async def create_mentor(self) -> None:
        raise NotImplementedError()

    async def list_mentors(self) -> None:
        raise NotImplementedError()

    async def get_mentor(self, mentor_id: str) -> None:
        raise NotImplementedError()

    async def update_mentor(self, mentor_id: str) -> None:
        raise NotImplementedError()

    async def delete_mentor(self, mentor_id: str) -> None:
        raise NotImplementedError()
