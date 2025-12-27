from math import ceil
from result import Err, is_err, Ok, Result
from structlog.stdlib import get_logger

from src.database.model.feature_switch_model import FeatureSwitch, UpdateFeatureSwitchParams
from src.database.repository.feature_switch_repository import FeatureSwitchRepository
from src.database.repository.hackathon.participants_repository import ParticipantsRepository
from src.database.repository.hackathon.teams_repository import TeamsRepository
from src.exception import (
    FeatureSwitchNotFoundError,
)

from src.service.hackathon.team_service import TeamService
from src.service.constants import *

LOG = get_logger()


# TODO: This class should be split into multimple smaller ones as it breaks the Single Responsibility Principle
class HackathonUtilityService:
    """Service layer designed to hold all business logic related to hackathon management"""

    def __init__(
        self,
        participants_repo: ParticipantsRepository,
        teams_repo: TeamsRepository,
        team_service: TeamService,
        feature_switch_repo: FeatureSwitchRepository,
    ) -> None:
        self._participant_repo = participants_repo
        self._teams_repo = teams_repo
        self._fs_repo = feature_switch_repo
        self._team_service = team_service

    async def check_capacity_register_admin_participant_case(self) -> bool:
        """Calculate if there is enough capacity to register a new team. Capacity is measured in max number of verified
        teams in the hackathon. This is the Capacity Check 2 from the Excalidraw 'Adding a participant workflow'"""

        # Fetch number of verified random participants
        verified_random_participants = await self._participant_repo.get_verified_random_participants_count()

        # Fetch number of verified registered teams
        verified_registered_teams = await self._teams_repo.get_verified_registered_teams_count()

        # Calculate the anticipated number of teams
        number_ant_teams = verified_registered_teams + ceil(verified_random_participants / MAX_NUMBER_OF_TEAM_MEMBERS)

        # Check against the hackathon capacity
        return number_ant_teams < MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON

    async def check_capacity_register_random_participant_case(self) -> bool:
        """Calculate if there is enough capacity to register a new random participant. Capacity is measured in max
        number of verified teams in the hackathon. This is the Capacity Check 1 from the Excalidraw 'Adding a
        participant workflow'"""

        # Fetch number of verified random participants
        verified_random_participants = await self._participant_repo.get_verified_random_participants_count()

        # Fetch number of verified registered teams
        verified_registered_teams = await self._teams_repo.get_verified_registered_teams_count()

        # Calculate the anticipated number of teams if a new random participant is added
        number_ant_teams = verified_registered_teams + ceil(
            (verified_random_participants + 1) / MAX_NUMBER_OF_TEAM_MEMBERS
        )

        # Check against the hackathon capacity
        return number_ant_teams <= MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON

    async def close_reg_for_random_and_admin_participants(
        self,
    ) -> Result[FeatureSwitch, FeatureSwitchNotFoundError | Exception]:
        # Check if the feature switch exists
        feature_switch = await self._fs_repo.get_feature_switch(feature=REG_ADMIN_AND_RANDOM_SWITCH)

        if is_err(feature_switch):
            return feature_switch

        return await self._fs_repo.update(
            obj_id=str(feature_switch.ok_value.id), obj_fields=UpdateFeatureSwitchParams(state=True)
        )

    async def close_reg_for_all_participants(self) -> Result[FeatureSwitch, FeatureSwitchNotFoundError | Exception]:
        """
        Serves to close the hackathon registration for all kinds of participants: random, invite-link, and admin
        participants manually. Includes possible creation of random teams, if such process has not taken place
        automatically and flips the RegSwitch to false.

        Flipping the registration switch to false ultimately closes the registration. You can't use the registration
        API anymore. Moreover, there is also no front-end interface for it.
        """
        feature_switch = await self._fs_repo.update_by_name(
            name=REG_ALL_PARTICIPANTS_SWITCH, obj_fields=UpdateFeatureSwitchParams(state=False)
        )

        if is_err(feature_switch):
            return feature_switch

        # Now that we have disabled the switch we can run the random team creation process

        random_participant_teams_created = await self._team_service.create_random_participant_teams()

        if not random_participant_teams_created:
            return Err(Exception("Failed to create random participant teams"))

        return Ok(feature_switch.ok_value)
