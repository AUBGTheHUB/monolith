from datetime import datetime, timedelta
from datetime import timezone
from math import ceil
from typing import Optional, Tuple

from fastapi import BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorClientSession
from result import Err, is_err, Ok, Result
from structlog.stdlib import get_logger

from src.database.model.feature_switch_model import FeatureSwitch, UpdateFeatureSwitchParams
from src.database.model.hackathon.participant_model import Participant, UpdateParticipantParams
from src.database.model.hackathon.team_model import Team, UpdateTeamParams
from src.database.mongo.transaction_manager import MongoTransactionManager
from src.database.repository.feature_switch_repository import FeatureSwitchRepository
from src.database.repository.hackathon.participants_repository import ParticipantsRepository
from src.database.repository.hackathon.teams_repository import TeamsRepository
from src.environment import is_test_env, DOMAIN, is_local_env
from src.exception import (
    DuplicateTeamNameError,
    DuplicateEmailError,
    EmailRateLimitExceededError,
    ParticipantAlreadyVerifiedError,
    ParticipantNotFoundError,
    TeamNotFoundError,
    FeatureSwitchNotFoundError,
)
from src.server.schemas.request_schemas.schemas import (
    AdminParticipantInputData,
)
from src.service.hackathon.hackathon_mail_service import HackathonMailService
from src.service.hackathon.teams.team_service import TeamService
from src.service.jwt_utils.codec import JwtUtility
from src.service.jwt_utils.schemas import JwtParticipantInviteRegistrationData, JwtParticipantVerificationData
from src.service.constants import *

LOG = get_logger()


# TODO: This class should be split into multimple smaller ones as it breaks the Single Responsibility Principle
class HackathonService:
    """Service layer designed to hold all business logic related to hackathon management"""

    def __init__(
        self,
        participants_repo: ParticipantsRepository,
        teams_repo: TeamsRepository,
        team_service: TeamService,
        feature_switch_repo: FeatureSwitchRepository,
        tx_manager: MongoTransactionManager,
        mail_service: HackathonMailService,
        jwt_utility: JwtUtility,
    ) -> None:
        self._participant_repo = participants_repo
        self._teams_repo = teams_repo
        self._fs_repo = feature_switch_repo
        self._tx_manager = tx_manager
        self._mail_service = mail_service
        self._jwt_utility = jwt_utility
        self._team_service = team_service

    async def _create_participant_and_team_in_transaction_callback(
        self, input_data: AdminParticipantInputData, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[Tuple[Participant, Team], DuplicateEmailError | DuplicateTeamNameError | Exception]:
        """
        This method is intended to be passed as the `callback` argument to the `TransactionManager.with_transaction(...)`
        function.
        """

        team = await self._teams_repo.create(Team(name=input_data.team_name), session)

        if is_err(team):
            return team

        participant = await self._participant_repo.create(
            Participant(
                **input_data.model_dump(),
                team_id=team.ok_value.id,
            ),
            session,
        )
        if is_err(participant):
            return participant

        return Ok((participant.ok_value, team.ok_value))

    async def create_participant_and_team_in_transaction(
        self, input_data: AdminParticipantInputData
    ) -> Result[Tuple[Participant, Team], DuplicateEmailError | DuplicateTeamNameError | Exception]:
        """Creates a participant and team in a transactional manner. The participant is added to the team created. If
        any of the db operations: creation of a Team obj, creation of a Participant obj fails, the whole operation
        fails, and no permanent changes are made to the database."""

        return await self._tx_manager.with_transaction(
            self._create_participant_and_team_in_transaction_callback, input_data
        )

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

    async def check_team_capacity(self, team_id: str) -> bool:
        """Calculate if there is enough capacity to register a new participant from the invite link for his team."""

        # Fetch number of registered participants in the team
        registered_teammates = await self._participant_repo.get_number_registered_teammates(team_id)

        # Check against team capacity
        return registered_teammates + 1 <= MAX_NUMBER_OF_TEAM_MEMBERS

    async def verify_random_participant(
        self, jwt_data: JwtParticipantVerificationData
    ) -> Result[Tuple[Participant, None], ParticipantNotFoundError | ParticipantAlreadyVerifiedError | Exception]:

        # This step is taken to ensure that we are not verifying an already verified participant
        result = await self._participant_repo.fetch_by_id(jwt_data.sub)

        if is_err(result):
            return result

        if result.ok_value.email_verified:
            return Err(ParticipantAlreadyVerifiedError())

        # Updates the random participant if it exists
        result = await self._participant_repo.update(
            obj_id=jwt_data.sub, obj_fields=UpdateParticipantParams(email_verified=True)
        )

        if is_err(result):
            return result

        # As when first created, the random participant is not assigned to a team we return the team as None
        return Ok((result.ok_value, None))

    async def verify_admin_participant_and_team_in_transaction(
        self, jwt_data: JwtParticipantVerificationData
    ) -> Result[
        Tuple[Participant, Team],
        ParticipantNotFoundError | TeamNotFoundError | Exception,
    ]:
        return await self._tx_manager.with_transaction(self._verify_admin_participant_and_team_callback, jwt_data)

    async def _verify_admin_participant_and_team_callback(
        self,
        jwt_data: JwtParticipantVerificationData,
        session: Optional[AsyncIOMotorClientSession] = None,
    ) -> Result[
        Tuple[Participant, Team],
        ParticipantNotFoundError | TeamNotFoundError | ParticipantAlreadyVerifiedError | Exception,
    ]:
        # This step is taken to ensure that we are not verifying an already verified participant
        result = await self._participant_repo.fetch_by_id(jwt_data.sub)

        if is_err(result):
            return result

        if result.ok_value.email_verified:
            return Err(ParticipantAlreadyVerifiedError())

        result_verified_admin = await self._participant_repo.update(
            obj_id=jwt_data.sub, obj_fields=UpdateParticipantParams(email_verified=True), session=session
        )

        if is_err(result_verified_admin):
            return result_verified_admin

        result_verified_team = await self._teams_repo.update(
            obj_id=str(result_verified_admin.ok_value.team_id),
            obj_fields=UpdateTeamParams(is_verified=True),
            session=session,
        )

        if is_err(result_verified_team):
            return result_verified_team

        return Ok((result_verified_admin.ok_value, result_verified_team.ok_value))

    async def check_send_verification_email_rate_limit(self, participant_id: str) -> Result[
        Tuple[Participant, Team],
        ParticipantNotFoundError
        | TeamNotFoundError
        | ParticipantAlreadyVerifiedError
        | EmailRateLimitExceededError
        | Exception,
    ]:
        """Check if the verification email rate limit has been reached

        Returns:
            * A Tuple[Participant, Team] if the participant has not exceeded their email sending rate
            * A ParticipantNotFoundError if the participant resending the email is not found in the Database
            * A TeamNotFoundError if the team of the participant is not found in the Database
            * A ParticipantAlreadyVerifiedError if the participant has already been verified
            * An EmailRateLimitExceededError if the participant has exceeded their email sending rate
            * An Exception if some unexpected error occurred
        """

        participant = await self._participant_repo.fetch_by_id(obj_id=participant_id)

        # If there was an error fetching the participant return that error as it is as it will be handled further up by
        # the handler
        if is_err(participant):
            return participant

        # Check if the participant is already verified before sending another verification email
        if participant.ok_value.email_verified:
            return Err(ParticipantAlreadyVerifiedError())

        # We fetch the team so that we take advantage of the team info we have to pass to the mailing service
        team = (
            await self._teams_repo.fetch_by_id(obj_id=str(participant.ok_value.team_id))
            if participant.ok_value.is_admin
            else Ok(None)
        )

        # If there was an error fetching the team return that error as it is as it will be handled further up by the
        # handler
        if is_err(team):
            return team

        # The last_sent_mail field is None when there has not been any email sent previously
        if participant.ok_value.last_sent_verification_email is None:
            return Ok((participant.ok_value, team.ok_value))

        # Calculate the rate limit
        is_within_rate_limit = datetime.now() - participant.ok_value.last_sent_verification_email >= timedelta(
            seconds=RATE_LIMIT_SECONDS
        )

        # If it is not within the rate limit raise an error
        if not is_within_rate_limit:
            remaining_time = (
                RATE_LIMIT_SECONDS - (datetime.now() - participant.ok_value.last_sent_verification_email).seconds
            )

            return Err(EmailRateLimitExceededError(seconds_to_retry_after=remaining_time))

        return Ok((participant.ok_value, team.ok_value))

    async def send_verification_email(
        self, participant: Participant, background_tasks: BackgroundTasks, team: Team | None = None
    ) -> Result[Participant, ParticipantNotFoundError | ValueError | Exception] | None:
        """
        Sends a verification email to admin and random participants and adds a timestamp when the last verification
        email has been sent, for rate-limiting purposes
        Args:
            participant: the participant who should receive the email. Admin or random participant only, invite_link
                participants are automatically verified.
            team: The team which the admin participant created. Should be passed only when sending emails to admin
             participants, as random teams are created only after hackathon registration closes.
            background_tasks: This is passed initially from the routes as part of the FastAPI Dependency Injection
                system. It is auto-wired for us. We use background tasks as we want to send an email only once we
                have returned a response. In this way we are able to keep our response times sub-second as we don't
                wait for the email to be sent, which could take more than 2 seconds.
        Returns:
            * The updated Participant document (last_sent_verification_email and updated_at fields)

            * An Err if adding of the updating the participant document last_sent_verification_email property fails, or
            sending the verification emails fails.

            * None if we are in Test env, and we should not send emails
        """

        # Don't send emails when we are running tests
        if is_test_env():
            return None

        # Build the payload for the Jwt token
        expiration = int((datetime.now(timezone.utc) + timedelta(hours=24)).timestamp())
        payload = JwtParticipantVerificationData(sub=str(participant.id), is_admin=participant.is_admin, exp=expiration)

        # Create the Jwt Token
        jwt_token = self._jwt_utility.encode_data(data=payload)

        # Append the Jwt to the endpoint
        if is_local_env():
            verification_link = (
                f"http://{DOMAIN}:{FRONTEND_PORT}{PARTICIPANTS_VERIFICATION_ROUTE}?jwt_token={jwt_token}"
            )
        else:
            verification_link = f"https://{DOMAIN}{PARTICIPANTS_VERIFICATION_ROUTE}?jwt_token={jwt_token}"

        # Update the last_sent_verification_email field for rate-limiting purposes
        result = await self._participant_repo.update(
            obj_id=str(participant.id), obj_fields=UpdateParticipantParams(last_sent_verification_email=datetime.now())
        )

        # If the update fails, do not send the email and return the error (could happen if the participant is deleted
        # from the DB before it is updated, highly unlikely in PROD env)
        if is_err(result):
            return result

        err = self._mail_service.send_participant_verification_email(
            participant=result.ok_value,
            verification_link=verification_link,
            background_tasks=background_tasks,
            team_name=team.name if team else None,
        )

        if err is not None:
            return err

        # Return the updated participant
        return result

    def send_successful_registration_email(
        self, participant: Participant, background_tasks: BackgroundTasks, team: Team | None = None
    ) -> Err[ValueError] | None:
        """
        Sends an email confirming the successful registration of a participant.
        Args:
            participant: The participant who should receive the email. Could be admin, random or invite_link
             participant.
            team: The team which the admin participant created. Should be passed only when sending emails to admin or
             invite_link participants.
            background_tasks: This is passed initially from the routes as part of the FastAPI Dependency Injection
             system. It is auto-wired for us. We use background tasks as we want to send an email only once we have
             returned a response. In this way we are able to keep our response times sub-second as we don't wait for
             the email to be sent, which could take more than 2 seconds.
        Returns:
            An Err if sending the successful registration email fails
        """
        # Don't send emails when we are running tests
        if is_test_env():
            return None

        if team is None:
            # When dealing with random participants we no team_name and invite_link should be present in the email
            err = self._mail_service.send_participant_successful_registration_email(
                participant=participant, background_tasks=background_tasks
            )
            if err is not None:
                return err

            return None

        if participant.is_admin is False:
            # When dealing with invite_link participants we no invite_link should be present in the email
            err = self._mail_service.send_participant_successful_registration_email(
                participant=participant, team_name=team.name, background_tasks=background_tasks
            )
            if err is not None:
                return err

            return None

        # Build the payload for the Jwt token
        expiration = int((datetime.now(timezone.utc) + timedelta(days=15)).timestamp())
        payload = JwtParticipantInviteRegistrationData(
            sub=str(participant.id), team_id=str(team.id), team_name=team.name, exp=expiration
        )

        # Create the Jwt Token
        jwt_token = self._jwt_utility.encode_data(data=payload)

        # Append the Jwt to the endpoint
        if is_local_env():
            invite_link = f"http://{DOMAIN}:{FRONTEND_PORT}{PARTICIPANTS_REGISTRATION_ROUTE}?jwt_token={jwt_token}"
        else:
            invite_link = f"https://{DOMAIN}{PARTICIPANTS_REGISTRATION_ROUTE}?jwt_token={jwt_token}"

        err = self._mail_service.send_participant_successful_registration_email(
            participant=participant, background_tasks=background_tasks, invite_link=invite_link, team_name=team.name
        )
        if err is not None:
            return err

        return None

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
