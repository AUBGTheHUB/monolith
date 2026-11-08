from result import Err, Ok, Result
from structlog.stdlib import get_logger
from bson import ObjectId

from src.database.repository.tournament.groups_repository import GroupsRepository

from typing import Optional, cast

from pymongo.asynchronous.client_session import AsyncClientSession
from src.database.mongo.transaction_manager import MongoTransactionManager
from src.service.hackathon.team_service import TeamService

from src.database.model.tournament.group_model import Group, GroupUpdateParams

LOG = get_logger()


class GroupService:
    """Service layer responsible for tournament group operations."""

    def __init__(
        self,
        groups_repo: GroupsRepository,
        team_service: TeamService,
        tx_manager: MongoTransactionManager,
    ) -> None:
        self._groups_repo = groups_repo
        self._team_service = team_service
        self._tx_manager = tx_manager

    async def fetch_all_groups(self) -> Result[list[Group], Exception]:
        return await self._groups_repo.fetch_all()

    async def fetch_group_by_id(self, group_id: str) -> Result[Group, Err]:
        return await self._groups_repo.fetch_by_id(obj_id=group_id)

    async def fetch_inactive_groups(self) -> Result[list[Group], Exception]:
        """Fetch groups where a winner has already been declared."""
        groups_result = await self._groups_repo.fetch_all()

        match groups_result:
            case Err(error):
                return Err(error)
            case Ok(groups):
                return Ok([group for group in groups if group.winner_id is not None])

    async def fetch_active_groups(self) -> Result[list[Group], Exception]:
        """Fetch groups where no winner has been declared yet."""
        groups_result = await self._groups_repo.fetch_all()

        match groups_result:
            case Err(error):
                return Err(error)
            case Ok(groups):
                return Ok([group for group in groups if group.winner_id is None])

    async def generate_bracket(self) -> Result[list[Group], Exception]:
        """Generate the first round of the tournament bracket."""

        # Check whether a bracket already exists
        existing_groups = await self._groups_repo.fetch_all()

        match existing_groups:
            case Err(error):
                return Err(error)
            case Ok(groups):
                if groups:
                    return Ok(groups)

        # Fetch all teams
        teams_result = await self._team_service.fetch_all_teams()

        match teams_result:
            case Err(error):
                return Err(error)
            case Ok(teams):
                if len(teams) != 8:
                    return Err(ValueError("A tournament bracket requires exactly 8 teams."))

        # Create four groups for the first round
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

            match result:
                case Err(error):
                    return Err(error)
                case Ok(created_group):
                    created_groups.append(created_group)

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

        match group_result:
            case Err(error):
                return cast(
                    Result[Group, Exception],
                    cast(object, Err(error)),
                )
            case Ok(group):
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

        match update_result:
            case Err(error):
                return Err(error)
            case Ok(updated_group):
                if group.round >= 3:
                    return Ok(updated_group)

        next_round = group.round + 1
        next_bracket_number = (group.bracket_number + 1) // 2

        groups_result = await self._groups_repo.fetch_all(session=session)

        match groups_result:
            case Err(error):
                return Err(error)
            case Ok(groups):
                next_group = next(
                    (
                        item
                        for item in groups
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

        match next_group_result:
            case Err(error):
                return cast(
                    Result[Group, Exception],
                    cast(object, Err(error)),
                )
            case Ok(_):
                return Ok(updated_group)
