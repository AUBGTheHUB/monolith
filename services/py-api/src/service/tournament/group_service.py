from result import Err, Ok, Result, is_err
from typing import Any, Optional
from structlog.stdlib import get_logger
from bson import ObjectId
from src.database.repository.tournament.groups_repository import GroupsRepository
from src.service.tournament.tournament_registration_service import TournamentRegistrationService
from pymongo.asynchronous.client_session import AsyncClientSession
from src.database.mongo.transaction_manager import MongoTransactionManager
from src.database.model.tournament.group_model import Group, GroupUpdateParams

LOG = get_logger()


class GroupService:
    """Service layer responsible for tournament group operations."""

    def __init__(
        self,
        groups_repo: GroupsRepository,
        tournament_registration_service: TournamentRegistrationService,
        tx_manager: MongoTransactionManager,
    ) -> None:
        self._groups_repo = groups_repo
        self._tournament_registration_service = tournament_registration_service
        self._tx_manager = tx_manager

    async def _groups_with_team_names(
        self,
        groups: list[Group],
    ) -> Result[list[dict[str, Any]], Exception]:
        teams_result = await self._tournament_registration_service.fetch_all_teams()

        if is_err(teams_result):
            return Err(teams_result.err_value)

        teams_by_id = {str(team.id): team.name for team in teams_result.ok_value}

        enriched_groups = []

        for group in groups:
            group_data = group.dump_as_json()

            group_data["first_team_name"] = (
                teams_by_id.get(str(group.first_team_id)) if group.first_team_id is not None else None
            )

            group_data["second_team_name"] = (
                teams_by_id.get(str(group.second_team_id)) if group.second_team_id is not None else None
            )

            enriched_groups.append(group_data)

        return Ok(enriched_groups)

    async def fetch_all_groups(self) -> Result[list[dict[str, Any]], Exception]:
        groups_result = await self._groups_repo.fetch_all()

        if is_err(groups_result):
            return Err(groups_result.err_value)

        return await self._groups_with_team_names(groups_result.ok_value)

    async def fetch_group_by_id(
        self,
        group_id: ObjectId,
    ) -> Result[dict[str, Any], Exception]:
        group_result = await self._groups_repo.fetch_by_id(obj_id=group_id)

        if is_err(group_result):
            return Err(group_result.err_value)

        enriched_result = await self._groups_with_team_names([group_result.ok_value])

        if is_err(enriched_result):
            return Err(enriched_result.err_value)

        return Ok(enriched_result.ok_value[0])

    async def fetch_inactive_groups(self) -> Result[list[dict[str, Any]], Exception]:
        groups_result = await self._groups_repo.fetch_all()

        if is_err(groups_result):
            return Err(groups_result.err_value)

        inactive_groups = [group for group in groups_result.ok_value if group.winner_id is not None]

        return await self._groups_with_team_names(inactive_groups)

    async def fetch_active_groups(self) -> Result[list[dict[str, Any]], Exception]:
        groups_result = await self._groups_repo.fetch_all()

        if is_err(groups_result):
            return Err(groups_result.err_value)

        active_groups = [group for group in groups_result.ok_value if group.winner_id is None]

        return await self._groups_with_team_names(active_groups)

    async def generate_bracket(self) -> Result[list[dict[str, Any]], Exception]:
        """Generate the first round of the tournament bracket."""
        existing_groups = await self._groups_repo.fetch_all()

        if is_err(existing_groups):
            return Err(existing_groups.err_value)

        if existing_groups.ok_value:
            return await self._groups_with_team_names(existing_groups.ok_value)

        teams_result = await self._tournament_registration_service.fetch_all_teams()

        if is_err(teams_result):
            return Err(teams_result.err_value)

        teams = teams_result.ok_value

        if len(teams) != 8:
            return Err(ValueError("A tournament bracket requires exactly 8 teams."))

        groups_to_create = [
            Group(
                round=1,
                bracket_number=i + 1,
                first_team_id=teams[i * 2].id,
                second_team_id=teams[i * 2 + 1].id,
            )
            for i in range(4)
        ]

        creation_result = await self._tx_manager.with_transaction(
            self._create_groups_in_transaction,
            groups_to_create,
        )

        if is_err(creation_result):
            return Err(creation_result.err_value)

        return await self._groups_with_team_names(creation_result.ok_value)

    async def _create_groups_in_transaction(
        self,
        groups: list[Group],
        session: Optional[AsyncClientSession] = None,
    ) -> Result[list[Group], Exception]:
        created_groups = []

        for group in groups:
            result = await self._groups_repo.create(
                obj=group,
                session=session,
            )

            if is_err(result):
                return Err(result.err_value)

            created_groups.append(result.ok_value)

        return Ok(created_groups)

    async def declare_winner(
        self,
        group_id: str,
        winner_id: str,
    ) -> Result[dict[str, Any], Exception]:
        result = await self._tx_manager.with_transaction(
            self._declare_winner_in_transaction,
            group_id,
            winner_id,
        )

        if is_err(result):
            return Err(result.err_value)

        enriched_result = await self._groups_with_team_names([result.ok_value])

        if is_err(enriched_result):
            return Err(enriched_result.err_value)

        return Ok(enriched_result.ok_value[0])

    async def _declare_winner_in_transaction(
        self,
        group_id: str,
        winner_id: str,
        session: Optional[AsyncClientSession] = None,
    ) -> Result[Group, Exception]:
        group_result = await self._groups_repo.fetch_by_id(
            obj_id=group_id,
            session=session,
        )

        if is_err(group_result):
            return Err(group_result.err_value)

        group = group_result.ok_value

        if group.winner_id is not None:
            return Err(ValueError("A winner has already been declared."))

        if group.first_team_id is None or group.second_team_id is None:
            return Err(ValueError("Both teams must be assigned before declaring a winner."))

        if not ObjectId.is_valid(winner_id):
            return Err(ValueError("Invalid winner ID."))

        winner_object_id = ObjectId(winner_id)

        if winner_object_id not in (
            group.first_team_id,
            group.second_team_id,
        ):
            return Err(ValueError("Winner must be one of the two teams."))

        update_result = await self._groups_repo.update(
            obj_id=group_id,
            obj_fields=GroupUpdateParams(winner_id=winner_object_id),
            session=session,
        )

        if is_err(update_result):
            return Err(update_result.err_value)

        updated_group = update_result.ok_value

        if group.round >= 3:
            return Ok(updated_group)

        next_round = group.round + 1
        next_bracket_number = (group.bracket_number + 1) // 2

        groups_result = await self._groups_repo.fetch_all(session=session)

        if is_err(groups_result):
            return Err(groups_result.err_value)

        next_group = next(
            (
                item
                for item in groups_result.ok_value
                if item.round == next_round and item.bracket_number == next_bracket_number
            ),
            None,
        )

        field_to_update = "first_team_id" if group.bracket_number % 2 == 1 else "second_team_id"

        update_params = GroupUpdateParams(**{field_to_update: winner_object_id})

        if next_group is None:
            new_group = Group(
                round=next_round,
                bracket_number=next_bracket_number,
                **{field_to_update: winner_object_id},
            )

            next_group_result = await self._groups_repo.create(
                obj=new_group,
                session=session,
            )
        else:
            next_group_result = await self._groups_repo.update(
                obj_id=str(next_group.id),
                obj_fields=update_params,
                session=session,
            )

        if is_err(next_group_result):
            return Err(next_group_result.err_value)

        return Ok(updated_group)
