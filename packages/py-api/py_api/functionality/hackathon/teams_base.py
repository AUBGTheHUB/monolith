from typing import Any, Dict, List, Tuple

from bson import ObjectId
from py_api.database.initialize import client, t_col

# from py_api.functionality.hackathon.custom_exceptions import TeamUpdateException
from py_api.models import HackathonTeam
from py_api.models.hackathon_teams_models import TeamType
from pymongo import results
from pymongo.client_session import ClientSession


class TeamFunctionality:

    @classmethod
    def create_team_object_with_first_participant(
            cls, user_id: str,
            team_name: str | None = None, generate_random_team: bool = False,
    ) -> HackathonTeam:
        """ creates a new HackathonTeam object without inserting it in the database """

        team_type = TeamType.NORMAL

        if generate_random_team:
            # Generate a team of type RANDOM for participants who are signing up themselves individually
            team_type = TeamType.RANDOM
            team_name = cls.generate_random_team_name()

        # Upon team initialization, we need at least one team member
        team_members_ids = [user_id]

        new_team = HackathonTeam(
            team_name=team_name,
            team_type=team_type, team_members=team_members_ids, is_verified=True,
        )

        return new_team

    @classmethod
    def add_participant_to_team_object(
            cls, team_name: str,
            user_id: str,
    ) -> Tuple[Dict[str, str], int] | HackathonTeam:
        """ fetches a HackathonTeam object and updates it without inserting it back in the database

        Returns a tuple with a message and a status code if an error occurred"""

        team = cls.fetch_team(team_name=team_name)

        if not team:
            return {"message": "Team with such name does not exist"}, 404

        if len(team.team_members) == 6:
            return {"message": "Team is already at max capacity"}, 409

        team.team_members.append(user_id)

        return team

    @classmethod
    def fetch_team(
            cls, team_name: str | None = None,
            team_id: str | None = None,
    ) -> HackathonTeam | None:

        team: Dict[str, Any] = {}

        if team_name:
            team = t_col.find_one(
                filter={"team_name": team_name},
            )

        elif team_id:
            team = t_col.find_one(filter={"_id": ObjectId(team_id)})

        if not team:
            return None

        return HackathonTeam(**team)

    @classmethod
    def fetch_teams_by_condition(cls, conditions: Dict[str, Any]) -> List[HackathonTeam]:
        # if conditions are empty it will return all the teams
        filtered_teams = list(t_col.find(conditions))
        return [HackathonTeam(**team) for team in filtered_teams]

    @classmethod
    def _update_team(
            cls, query: Dict[str, Any], team_payload: Dict[str, Any],
            session: ClientSession = None,
    ) -> HackathonTeam:
        updated_team = t_col.find_one_and_update(
            query, {
                "$set": {
                    key: value for key, value in team_payload.items() if value
                },
            }, projection={"_id": 0}, return_document=True, session=session,
        )
        return HackathonTeam(**updated_team)

    @classmethod
    def update_team_query_using_dump(
            cls, team_payload: Dict[str, Any], object_id: str | None = None,
            session: ClientSession | None = None,
    ) -> HackathonTeam:

        query = {
            "$or": [
                {"_id": ObjectId(object_id)},
                {"team_name": team_payload.get("team_name")},
            ],
        }

        if session:
            return cls._update_team(query, team_payload, session)

        with client.start_session() as session:
            with session.start_transaction():
                return cls._update_team(query, team_payload, session)

    @classmethod
    def generate_random_team_name(cls) -> str:
        count = t_col.count_documents({"team_type": "random"})
        return f"RandomTeam {count + 1}"

    @classmethod
    def insert_team(cls, team: HackathonTeam, session: ClientSession) -> results.InsertOneResult:
        return t_col.insert_one(team.model_dump(), session=session)

    @classmethod
    def delete_team(cls, object_id: str) -> results.DeleteResult | None:
        with client.start_session() as session:
            with session.start_transaction():
                return t_col.find_one_and_delete(
                    filter={"_id": ObjectId(object_id)}, session=session,
                )

    @classmethod
    def get_count_of_teams(cls) -> int:
        """Counts the number of verified teams in the database"""
        return len(cls.fetch_teams_by_condition({"is_verified": True}))
