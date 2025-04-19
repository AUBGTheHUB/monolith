from datetime import datetime, timedelta
from datetime import timezone
from math import ceil
from secrets import token_hex
from typing import Final, Optional, Tuple, List, TypedDict

from fastapi import BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorClientSession
from result import Err, is_err, Ok, Result
from structlog.stdlib import get_logger

from src.database.model.base_model import SerializableObjectId
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
    TeamNameMissmatchError,
    TeamNotFoundError,
    FeatureSwitchNotFoundError,
)
from src.server.schemas.request_schemas.schemas import (
    RandomParticipantInputData,
    AdminParticipantInputData,
    InviteLinkParticipantInputData,
)
from src.service.hackathon.hackathon_mail_service import HackathonMailService
from src.service.jwt_utils.codec import JwtUtility
from src.service.jwt_utils.schemas import JwtParticipantInviteRegistrationData, JwtParticipantVerificationData

LOG = get_logger()


# TODO: This should be moved when splitting HackathonService
class RandomTeam(TypedDict):
    team: Team
    participants: list[Participant]


# TODO: This class should be split into multimple smaller ones as it breaks the Single Responsibility Principle
class HackathonService:
    """Service layer designed to hold all business logic related to hackathon management"""

    MAX_NUMBER_OF_TEAM_MEMBERS: Final[int] = 6
    """Constraint for max number of participants in a given team"""

    MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON: Final[int] = 16
    """Constraint for max number of verified teams in the hackathon. A team is verified when the admin participant who
    created the team, verified their email. This const also includes the random teams, which are automatically created
    and marked as verified, once the hackathon registration closes"""

    REG_ADMIN_AND_RANDOM_SWITCH: Final[str] = "isRegTeamsFull"
    """This switch toggles the registration for the admin and random participants. It will disable the application
    form in the frontend when it is set to `true` and it will enable it when it is set to `false`. If somebody tries to
    register using the API endpoint they will get the `Max hackathon capacity has been reached` message.
    """

    REG_ALL_PARTICIPANTS_SWITCH: Final[str] = "RegSwitch"
    """This switch toggles the registration for the all participants. It will disable the application for both
    the front-end interface and the API endpoint. If somebody tries to register through the API endpoint they will get
    the `Registration is closed` message.
    """

    _RATE_LIMIT_SECONDS: Final[int] = 90
    """Number of seconds before a participant is allowed to resend their verification email, if they didn't get one."""

    _PARTICIPANTS_VERIFICATION_ROUTE = "/hackathon/verification"
    """The front-end route for email verification"""

    _PARTICIPANTS_REGISTRATION_ROUTE = "/hackathon/registration"
    """The front-end route for hackathon registration"""

    _FRONTEND_PORT = 3000
    """The port on which the frontend is running"""

    def __init__(
        self,
        participants_repo: ParticipantsRepository,
        teams_repo: TeamsRepository,
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

    async def create_random_participant(
        self, input_data: RandomParticipantInputData
    ) -> Result[Tuple[Participant, None], DuplicateEmailError | Exception]:

        result = await self._participant_repo.create(
            Participant(**input_data.model_dump(), is_admin=False, team_id=None)
        )
        if is_err(result):
            return result

        # As when first created, the random participant is not assigned to a team we return the team as None
        return Ok((result.ok_value, None))

    async def create_invite_link_participant(
        self, input_data: InviteLinkParticipantInputData, decoded_jwt_token: JwtParticipantInviteRegistrationData
    ) -> Result[Tuple[Participant, Team], DuplicateEmailError | TeamNotFoundError | TeamNameMissmatchError | Exception]:

        # Check if team still exists - Returns an error when it doesn't
        team_result = await self._teams_repo.fetch_by_id(decoded_jwt_token.team_id)
        if is_err(team_result):
            return team_result

        # Check if the team_name from the token is consistent with the team_name from the request body
        # A missmatch could occur if the frontend passes something different
        if input_data.team_name != team_result.ok_value.name:
            return Err(TeamNameMissmatchError())

        participant_result = await self._participant_repo.create(
            Participant(
                **input_data.model_dump(),
                team_id=SerializableObjectId(decoded_jwt_token.team_id),
                email_verified=True,
            )
        )
        if is_err(participant_result):
            return participant_result

        # Return the new participant
        return Ok((participant_result.ok_value, team_result.ok_value))

    async def check_capacity_register_admin_participant_case(self) -> bool:
        """Calculate if there is enough capacity to register a new team. Capacity is measured in max number of verified
        teams in the hackathon. This is the Capacity Check 2 from the Excalidraw 'Adding a participant workflow'"""

        # Fetch number of verified random participants
        verified_random_participants = await self._participant_repo.get_verified_random_participants_count()

        # Fetch number of verified registered teams
        verified_registered_teams = await self._teams_repo.get_verified_registered_teams_count()

        # Calculate the anticipated number of teams
        number_ant_teams = verified_registered_teams + ceil(
            verified_random_participants / self.MAX_NUMBER_OF_TEAM_MEMBERS
        )

        # Check against the hackathon capacity
        return number_ant_teams < self.MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON

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
            (verified_random_participants + 1) / self.MAX_NUMBER_OF_TEAM_MEMBERS
        )

        # Check against the hackathon capacity
        return number_ant_teams <= self.MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON

    async def check_team_capacity(self, team_id: str) -> bool:
        """Calculate if there is enough capacity to register a new participant from the invite link for his team."""

        # Fetch number of registered participants in the team
        registered_teammates = await self._participant_repo.get_number_registered_teammates(team_id)

        # Check against team capacity
        return registered_teammates + 1 <= self.MAX_NUMBER_OF_TEAM_MEMBERS

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

    async def delete_participant(
        self, participant_id: str
    ) -> Result[Participant, ParticipantNotFoundError | Exception]:
        return await self._participant_repo.delete(obj_id=participant_id)

    async def fetch_all_teams(self) -> Result[List[Team], Exception]:
        return await self._teams_repo.fetch_all()

    async def delete_team(self, team_id: str) -> Result[Team, TeamNotFoundError | Exception]:
        return await self._teams_repo.delete(obj_id=team_id)

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
            seconds=self._RATE_LIMIT_SECONDS
        )

        # If it is not within the rate limit raise an error
        if not is_within_rate_limit:
            remaining_time = (
                self._RATE_LIMIT_SECONDS - (datetime.now() - participant.ok_value.last_sent_verification_email).seconds
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
                f"http://{DOMAIN}:{self._FRONTEND_PORT}{self._PARTICIPANTS_VERIFICATION_ROUTE}?jwt_token={jwt_token}"
            )
        else:
            verification_link = f"https://{DOMAIN}{self._PARTICIPANTS_VERIFICATION_ROUTE}?jwt_token={jwt_token}"

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
            invite_link = (
                f"http://{DOMAIN}:{self._FRONTEND_PORT}{self._PARTICIPANTS_REGISTRATION_ROUTE}?jwt_token={jwt_token}"
            )
        else:
            invite_link = f"https://{DOMAIN}{self._PARTICIPANTS_REGISTRATION_ROUTE}?jwt_token={jwt_token}"

        err = self._mail_service.send_participant_successful_registration_email(
            participant=participant, background_tasks=background_tasks, invite_link=invite_link, team_name=team.name
        )
        if err is not None:
            return err

        return None

    async def create_random_participant_teams(self) -> bool:

        result = await self.retrieve_and_categorize_random_participants()

        if is_err(result):
            return False

        (prog_participants, non_prog_participants) = result.ok_value

        random_teams = self.form_random_participant_teams(prog_participants, non_prog_participants)

        result = await self.create_random_participant_teams_in_transaction(random_teams)

        if is_err(result):
            return False

        return True

    async def retrieve_and_categorize_random_participants(
        self,
    ) -> Result[Tuple[List[Participant], List[Participant]], Exception]:
        programming_oriented = []
        non_programming_oriented = []
        # Fetch all the verified random participants
        result = await self._participant_repo.get_verified_random_participants()

        # Return the result to the upper layer in case of an Exception
        if is_err(result):
            return result

        # Group the into categories programming oriented, non-programming oriented
        for participant in result.ok_value:
            if participant.programming_level == "I am not participating as a programmer":
                non_programming_oriented.append(participant)
            else:
                programming_oriented.append(participant)

        return Ok((programming_oriented, non_programming_oriented))

    def form_random_participant_teams(
        self, prog_participants: list[Participant], non_prog_participants: list[Participant]
    ) -> List[RandomTeam]:
        # Calculate the number of hackathon participants
        number_of_random_participants = len(prog_participants) + len(non_prog_participants)
        # Calculate the number of teams that are going to be needed for the given number of participants
        number_of_teams = ceil(number_of_random_participants / self.MAX_NUMBER_OF_TEAM_MEMBERS)

        # Create a list for storing the Random Teams
        teams = []

        # Populate the dictionary with the Random Teams named `RandomTeam{i}`
        for i in range(number_of_teams):
            teams.append(RandomTeam(team=Team(name=f"RT_{token_hex(8)}", is_verified=True), participants=[]))

        # Spread all the programming experienced participants to the teams in a Round Robin (RR) manner
        ctr = 0  # initialize a counter
        while len(prog_participants) > 0:
            teams[ctr % number_of_teams]["participants"].append(prog_participants.pop())
            ctr += 1

        # Spread all the non-programming experienced participants to the teams in a Round Robin (RR) manner
        ctr = 0  # reset counter
        while len(non_prog_participants) > 0:
            teams[ctr % number_of_teams]["participants"].append(non_prog_participants.pop())
            ctr += 1

        return teams

    async def _create_random_participant_teams_in_transaction_callback(
        self, random_teams: List[RandomTeam], session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[List[RandomTeam], DuplicateTeamNameError | ParticipantNotFoundError | Exception]:
        # Loop through each RandomTeam in the list. Create the team. Update all the participants with the id of the team
        # created
        for random_team in random_teams:
            # Create the team
            team_result = await self._teams_repo.create(team=random_team["team"], session=session)

            if is_err(team_result):
                return team_result

            # Take out one of the participants and assign them as an admin in the newly created random team
            admin_participant = random_team["participants"].pop()
            admin_result = await self._participant_repo.update(
                obj_id=str(admin_participant.id),
                obj_fields=UpdateParticipantParams(team_id=random_team["team"].id, is_admin=True),
                session=session,
            )

            if is_err(admin_result):
                return admin_result

            # Insert all the participants in the team that was created
            update_result = await self._participant_repo.bulk_update(
                obj_ids=[participant.id for participant in random_team["participants"]],
                obj_fields=UpdateParticipantParams(team_id=random_team["team"].id),
            )

            if is_err(update_result):
                return update_result

        return Ok(random_teams)

    async def create_random_participant_teams_in_transaction(
        self, input_data: List[RandomTeam]
    ) -> Result[List[RandomTeam], DuplicateTeamNameError | ParticipantNotFoundError | Exception]:
        return await self._tx_manager.with_transaction(
            self._create_random_participant_teams_in_transaction_callback, input_data
        )

    async def close_reg_for_random_and_admin_participants(
        self,
    ) -> Result[FeatureSwitch, FeatureSwitchNotFoundError | Exception]:
        # Check if the feature switch exists
        feature_switch = await self._fs_repo.get_feature_switch(feature=self.REG_ADMIN_AND_RANDOM_SWITCH)

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
            name=self.REG_ALL_PARTICIPANTS_SWITCH, obj_fields=UpdateFeatureSwitchParams(state=False)
        )

        if is_err(feature_switch):
            return feature_switch

        # Now that we have disabled the switch we can run the random team creation process

        random_participant_teams_created = await self.create_random_participant_teams()

        if not random_participant_teams_created:
            return Err(Exception("Failed to create random participant teams"))

        return Ok(feature_switch.ok_value)
