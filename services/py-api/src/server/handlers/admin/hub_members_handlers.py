import json
from typing import Annotated

from fastapi import Form, UploadFile
from pydantic import StringConstraints
from result import is_err

from src.database.model.admin.hub_member_model import DEPARTMENTS_LIST, SocialLinks
from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.response_schemas.schemas import Response
from src.server.schemas.response_schemas.admin.hub_member_schemas import HubMemberResponse, AllHubMembersResponse
from src.service.admin.hub_members_service import HubMembersService
from starlette import status


class HubMembersHandlers(BaseHandler):
    def __init__(self, service: HubMembersService) -> None:
        self._service = service

    async def create_hub_member(
        self,
        name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1), Form(...)],
        position: Annotated[str | None, StringConstraints(strip_whitespace=True, min_length=1), Form(...)],
        departments: Annotated[list[DEPARTMENTS_LIST], Form()],
        avatar: Annotated[UploadFile, Form()],
        social_links: Annotated[str, Form()],
    ) -> Response:
        social_links_dict: SocialLinks = json.loads(social_links)

        result = await self._service.create(
            name=name, position=position, departments=departments, avatar=avatar, social_links=social_links_dict
        )

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=HubMemberResponse(hub_member=result.ok_value),
            status_code=status.HTTP_201_CREATED,
        )

    async def get_all_hub_members(self) -> Response:
        result = await self._service.get_all()
        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=AllHubMembersResponse(members=result.ok_value),
            status_code=status.HTTP_200_OK,
        )

    async def get_hub_member(self, object_id: str) -> Response:
        result = await self._service.get(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=HubMemberResponse(hub_member=result.ok_value),
            status_code=status.HTTP_200_OK,
        )

    async def update_hub_member(
        self,
        object_id: str,
        name: Annotated[str | None, StringConstraints(strip_whitespace=True, min_length=1), Form(...)] = None,
        position: Annotated[str | None, StringConstraints(strip_whitespace=True, min_length=1), Form(...)] = None,
        departments: Annotated[list[DEPARTMENTS_LIST] | None, Form()] = None,
        avatar: Annotated[UploadFile | None, Form()] = None,
        social_links: Annotated[str | None, Form()] = None,
    ) -> Response:
        if social_links is not None:
            social_links_dict: SocialLinks = json.loads(str(social_links))
        else:
            social_links_dict = {}
        result = await self._service.update(
            object_id,
            name=name,
            position=position,
            departments=departments,
            avatar=avatar,
            social_links=social_links_dict,
        )

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=HubMemberResponse(hub_member=result.ok_value),
            status_code=status.HTTP_200_OK,
        )

    async def delete_hub_member(self, object_id: str) -> Response:
        result = await self._service.delete(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=HubMemberResponse(hub_member=result.ok_value),
            status_code=status.HTTP_200_OK,
        )
