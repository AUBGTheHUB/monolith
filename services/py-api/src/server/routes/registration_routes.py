from fastapi import APIRouter, status
from src.database.registration_models import Participant


def register_registration_routes(http_handler) -> APIRouter:
    router = APIRouter(prefix="/registration", tags=["Registration"])

    @router.post("/team/admin", status_code=status.HTTP_201_CREATED)
    async def register_team_admin(participant: Participant, team_name: str):
        return await http_handler.register_team_admin_handler(participant, team_name)

    @router.post("/team/member", status_code=status.HTTP_201_CREATED)
    async def register_team_member(participant: Participant, team_code: str):
        return await http_handler.register_team_member_handler(participant, team_code)

    @router.post("/solo", status_code=status.HTTP_201_CREATED)
    async def register_solo(participant: Participant):
        return await http_handler.register_solo_handler(participant)

    @router.post("/team/backfill", status_code=status.HTTP_200_OK)
    async def backfill_teams():
        return await http_handler.backfill_teams_handler()

    return router
