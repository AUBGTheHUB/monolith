import secrets

from bson import ObjectId
from result import Result, Ok, Err, is_err, is_ok
from typing import Callable
from structlog.stdlib import get_logger
from src.database.model.event_registration.team_model import Team
from src.database.repository.event_registration.teams_repository import TeamsRepository
from src.database.mongo.transaction_manager import MongoTransactionManager
from src.database.model.event_registration.participant_model import Participant
from src.database.repository.event_registration.participants_repository import (
    ParticipantsRepository,
)

LOG = get_logger()

CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def generate_team_code() -> str:
    return "".join(secrets.choice(CODE_ALPHABET) for _ in range(8))


async def register_team_admin(
    participant_data: dict,
    team_name: str,
    participants_repository: ParticipantsRepository,
    teams_repository: TeamsRepository,
    transaction_manager: MongoTransactionManager,
) -> Result[Team, Exception]:

    data = participant_data.copy()
    data["email"] = str(data["email"]).strip().lower()

    async def operation(*, session):

        # Check whether the participant is already registered.
        existing = await participants_repository.find_by_email(
            data["email"],
            session=session,
        )

        if is_err(existing):
            return Err(existing.err_value)

        if existing.ok_value is not None:
            return Err(ValueError("Participant is already registered"))

        # Find an unused joining code.
        code = None

        for _ in range(5):
            candidate = generate_team_code()

            lookup = await teams_repository.find_by_code(
                candidate,
                session=session,
            )

            if is_err(lookup):
                return Err(lookup.err_value)

            if lookup.ok_value is None:
                code = candidate
                break

        if code is None:
            return Err(ValueError("Could not generate an available team code"))

        # Create the team leader.
        leader = Participant(
            **data,
            is_team_leader=True,
        )

        # Create the team using the leader's database ID.
        team = Team(
            name=team_name,
            code=code,
            leader_id=leader.id,
        )

        # Link the leader to the new team.
        leader.team_id = team.id

        # Save the team.
        team_result = await teams_repository.create(
            team,
            session=session,
        )

        if is_err(team_result):
            return Err(team_result.err_value)

        # Save the leader.
        participant_result = await participants_repository.create(
            leader,
            session=session,
        )

        if is_err(participant_result):
            return Err(participant_result.err_value)

        return Ok(team)

    return await transaction_manager.with_transaction(operation)


async def register_team_member(
    participant_data: dict,
    team_code: str,
    participants_repository: ParticipantsRepository,
    teams_repository: TeamsRepository,
    transaction_manager: MongoTransactionManager,
    on_team_completed: Callable[[str, str, str], None] | None = None,
) -> Result[Participant, Exception]:

    data = participant_data.copy()
    data["email"] = str(data["email"]).strip().lower()

    team_code = team_code.strip().upper()

    completed_team = None

    async def operation(*, session):
        nonlocal completed_team
        completed_team = None

        # Prevent duplicate registrations.
        existing = await participants_repository.find_by_email(
            data["email"],
            session=session,
        )

        if is_err(existing):
            return Err(existing.err_value)

        if existing.ok_value is not None:
            return Err(ValueError("Participant is already registered"))

        # Reserve one of the five team places.
        slot_result = await teams_repository.reserve_slot(
            team_code,
            session=session,
        )

        if is_err(slot_result):
            return Err(slot_result.err_value)

        if slot_result.ok_value is None:

            lookup = await teams_repository.find_by_code(
                team_code,
                session=session,
            )

            if is_err(lookup):
                return Err(lookup.err_value)

            if lookup.ok_value is None:
                return Err(ValueError("Invalid team code"))

            return Err(ValueError("Team is full"))

        team_document = slot_result.ok_value

        # Create the new team member.
        participant = Participant(
            **data,
            team_id=team_document["_id"],
            is_team_leader=False,
        )

        # Save the participant.
        result = await participants_repository.create(
            participant,
            session=session,
        )

        if is_err(result):
            return Err(result.err_value)

        # Mark the team complete when the fifth member joins.
        if team_document["member_count"] == 5:

            completion_result = await teams_repository.mark_completed(
                team_code,
                session=session,
            )

            if is_err(completion_result):
                return Err(completion_result.err_value)

            if completion_result.ok_value is not None:
                completed_team = completion_result.ok_value

        return Ok(participant)

    # Execute the entire registration transaction.
    result = await transaction_manager.with_transaction(operation)

    # Only queue the email after a successful transaction.
    if is_ok(result) and completed_team is not None and on_team_completed is not None:
        try:
            leader_result = await participants_repository.find_by_id(completed_team["leader_id"])

            if is_err(leader_result):
                LOG.error(
                    "Could not retrieve team leader for completion email",
                    error=leader_result.err_value,
                )

            elif leader_result.ok_value is None:
                LOG.error(
                    "Team leader not found for completion email",
                    team_code=team_code,
                )

            else:
                on_team_completed(
                    leader_result.ok_value["email"],
                    completed_team["name"],
                    completed_team["code"],
                )

        except Exception as error:
            LOG.exception(
                "Could not queue team completion email",
                error=error,
                team_code=team_code,
            )

    return result


async def register_solo_member(
    participant_data: dict,
    participants_repository: ParticipantsRepository,
) -> Result[Participant, Exception]:

    data = participant_data.copy()

    # Normalize email before checking or saving it.
    data["email"] = str(data["email"]).strip().lower()

    existing_result = await participants_repository.find_by_email(data["email"])

    if is_err(existing_result):
        return Err(existing_result.err_value)

    if existing_result.ok_value is not None:
        return Err(ValueError("Participant is already registered"))

    participant = Participant(
        **data,
        team_id=None,
        is_team_leader=False,
        assigned_role=None,
    )

    return await participants_repository.create(participant)


async def assign_solo_member_to_team(
    participant_id: str,
    team_code: str,
    assigned_role: str,
    participants_repository: ParticipantsRepository,
    teams_repository: TeamsRepository,
    transaction_manager: MongoTransactionManager,
    on_team_completed: Callable[[str, str, str], None] | None = None,
) -> Result[dict, Exception]:

    if not ObjectId.is_valid(participant_id):
        return Err(ValueError("Invalid participant ID"))

    assigned_role = assigned_role.strip()

    if not assigned_role:
        return Err(ValueError("Assigned role cannot be empty"))

    team_code = team_code.strip().upper()
    participant_object_id = ObjectId(participant_id)

    completed_team = None

    async def operation(*, session):
        nonlocal completed_team

        completed_team = None

        # 1. Find the participant.
        participant_result = await participants_repository.find_by_id(
            participant_object_id,
            session=session,
        )

        if is_err(participant_result):
            return Err(participant_result.err_value)

        participant_document = participant_result.ok_value

        if participant_document is None:
            return Err(ValueError("Participant not found"))

        # 2. Only individually registered participants can be assigned.
        if participant_document.get("team_id") is not None:
            return Err(ValueError("Participant already belongs to a team"))

        # 3. Reserve a team place.
        slot_result = await teams_repository.reserve_slot(
            team_code,
            session=session,
        )

        if is_err(slot_result):
            return Err(slot_result.err_value)

        if slot_result.ok_value is None:
            lookup = await teams_repository.find_by_code(
                team_code,
                session=session,
            )

            if is_err(lookup):
                return Err(lookup.err_value)

            if lookup.ok_value is None:
                return Err(ValueError("Invalid team code"))

            return Err(ValueError("Team is full"))

        team_document = slot_result.ok_value

        # 4. Attach the participant to the team.
        assignment_result = await participants_repository.assign_solo_to_team(
            participant_id=participant_object_id,
            team_id=team_document["_id"],
            assigned_role=assigned_role,
            session=session,
        )

        if is_err(assignment_result):
            return Err(assignment_result.err_value)

        if assignment_result.ok_value is None:
            return Err(ValueError("Participant could not be assigned"))

        # 5. Check whether this was the fifth member.
        if team_document["member_count"] == 5:
            completion_result = await teams_repository.mark_completed(
                team_code,
                session=session,
            )

            if is_err(completion_result):
                return Err(completion_result.err_value)

            if completion_result.ok_value is not None:
                completed_team = completion_result.ok_value

        return Ok(assignment_result.ok_value)

    # 6. Commit the database changes together.
    result = await transaction_manager.with_transaction(operation)

    # 7. Queue the completion email only after a successful commit.
    if is_ok(result) and completed_team is not None and on_team_completed is not None:
        try:
            leader_result = await participants_repository.find_by_id(completed_team["leader_id"])

            if is_err(leader_result):
                LOG.error(
                    "Could not retrieve team leader for completion email",
                    error=leader_result.err_value,
                )

            elif leader_result.ok_value is None:
                LOG.error(
                    "Team leader not found for completion email",
                    team_code=team_code,
                )

            else:
                on_team_completed(
                    leader_result.ok_value["email"],
                    completed_team["name"],
                    completed_team["code"],
                )

        except Exception as error:
            LOG.exception(
                "Could not queue team completion email",
                error=error,
                team_code=team_code,
            )

    return result
