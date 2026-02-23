from fastapi import UploadFile
from result import Result

from src.database.model.admin.hub_member_model import HubMember, DEPARTMENTS_LIST, SocialLinks
from src.database.repository.admin.hub_members_repository import HubMembersRepository
from src.database.model.admin.hub_member_model import UpdateHubMemberParams
from src.server.schemas.request_schemas.schemas import NonEmptyStr
from src.service.utility.image_storing.image_storing_service import ImageStoringService


class HubMembersService:
    def __init__(self, repo: HubMembersRepository, image_storing_service: ImageStoringService) -> None:
        self._repo = repo
        self._image_storing_service = image_storing_service

    async def get_all(self) -> Result[list[HubMember], Exception]:
        return await self._repo.fetch_all()

    async def get(self, member_id: str) -> Result[HubMember, Exception]:
        return await self._repo.fetch_by_id(member_id)

    async def create(
        self,
        name: NonEmptyStr,
        position: NonEmptyStr,
        departments: list[DEPARTMENTS_LIST],
        avatar: UploadFile,
        social_links: SocialLinks,
    ) -> Result[HubMember, Exception]:
        member = HubMember(
            name=name,
            position=position,
            departments=departments,
            avatar_url="",
            social_links=social_links,
        )
        avatar_url = await self._image_storing_service.upload_image(avatar, f"hub-members/{str(member.id)}")
        member.avatar_url = str(avatar_url)
        return await self._repo.create(member)

    async def update(
        self,
        member_id: str,
        name: NonEmptyStr | None = None,
        position: NonEmptyStr | None = None,
        departments: list[DEPARTMENTS_LIST] | None = None,
        avatar: UploadFile | None = None,
        social_links: SocialLinks | None = None,
    ) -> Result[HubMember, Exception]:

        if avatar is not None:
            await self._image_storing_service.upload_image(file=avatar, file_name=f"hub-members/{str(member_id)}")
        update_params = UpdateHubMemberParams(
            name=name, position=position, departments=departments, social_links=social_links
        )
        return await self._repo.update(member_id, update_params)

    async def delete(self, member_id: str) -> Result[HubMember, Exception]:
        result = await self._repo.delete(member_id)

        if result.is_ok():
            self._image_storing_service.delete_image(f"hub-members/{str(member_id)}")

        return result
