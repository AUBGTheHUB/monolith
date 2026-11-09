from result import Err, Ok, Result, is_err
from structlog.stdlib import get_logger
from bson import ObjectId

from src.database.repository.tournament.groups_repository import GroupsRepository

from typing import Optional

from pymongo.asynchronous.client_session import AsyncClientSession
from src.database.mongo.transaction_manager import MongoTransactionManager
from src.database.repository.tournament.tournament_teams_repository import TournamentTeamsRepository
from src.database.model.tournament.group_model import Group, GroupUpdateParams

LOG = get_logger()


class GroupService:
    """Service layer responsible for tournament group operations."""

    def __init__(
        self,
        groups_repo: GroupsRepository,
        tournament_teams_repo: TournamentTeamsRepository,
        tx_manager: MongoTransactionManager,
    ) -> None:
        self._groups_repo = groups_repo
        self._tournament_teams_repo = tournament_teams_repo
        self._tx_manager = tx_manager

    async def fetch_all_groups(self) -> Result[list[Group], Exception]:
        return await self._groups_repo.fetch_all()

    async def fetch_group_by_id(self, group_id: str) -> Result[Group, Err]:
        return await self._groups_repo.fetch_by_id(obj_id=group_id)

    async def fetch_inactive_groups(self) -> Result[list[Group], Exception]:
        """Fetch groups where a winner has already been declared."""
        groups_result = await self._groups_repo.fetch_all()

        if is_err(groups_result):
            return Err(groups_result.err_value)

        return Ok([group for group in groups_result.ok_value if group.winner_id is not None])

    async def fetch_active_groups(self) -> Result[list[Group], Exception]:
        """Fetch groups where no winner has been declared yet."""
        groups_result = await self._groups_repo.fetch_all()

        if is_err(groups_result):
            return Err(groups_result.err_value)

        return Ok([group for group in groups_result.ok_value if group.winner_id is None])

    async def generate_bracket(self) -> Result[list[Group], Exception]:
        """Generate the first round of the tournament bracket."""
        existing_groups = await self._groups_repo.fetch_all()

        if is_err(existing_groups):
            return Err(existing_groups.err_value)

        if existing_groups.ok_value:
            return Ok(existing_groups.ok_value)

        teams_result = await self._tournament_teams_repo.fetch_all()

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

        return await self._tx_manager.with_transaction(
            self._create_groups_in_transaction,
            groups_to_create,
        )

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

    async def declare_winner(self, group_id: str, winner_id: str) -> Result[Group, Exception]:
        return await self._tx_manager.with_transaction(
            self._declare_winner_in_transaction,
            group_id,
            winner_id,
        )

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
