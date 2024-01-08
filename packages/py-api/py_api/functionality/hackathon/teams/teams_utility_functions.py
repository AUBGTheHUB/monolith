from typing import Any, Dict, List, Optional

from bson import ObjectId
from py_api.database.initialize import t_col
from py_api.models import HackathonTeam
from py_api.models.hackathon_teams_models import TeamType
from pymongo.results import UpdateResult


class TeamsUtilities:

    @classmethod
    def create_team(
            cls, user_id: str,
            team_name: str, ) -> HackathonTeam | None:
        team_type = TeamType.NORMAL

        if not team_name:
            # If no team_name is provided during registration, the participant is registering individually.
            # We create a team of type RANDOM which should be filled with such participants
            team_type = TeamType.RANDOM
            team_name = cls.generate_random_team_name()

        if cls.fetch_team(team_name=team_name):
            # A name with this team_name exist so no new team is created
            return None

        # The team is created with one person, and they are the admin of it
        team_members_ids = [user_id]

        new_team = HackathonTeam(
            team_name=team_name,
            team_type=team_type, team_members=team_members_ids,
        )
        t_col.insert_one(new_team.model_dump())

        return new_team

    @classmethod
    def add_participant_to_team(
        cls, team_name: str,
        user_id: str,
    ) -> HackathonTeam | None | str:
        team = cls.fetch_team(team_name=team_name)

        if not team:
            return None

        if len(team.team_members) == 6:
            return "No space left"  # TODO: This should be fixed

        team.team_members.append(user_id)

        return team

    @classmethod
    def fetch_team(
        cls, team_name: str = "",
        team_id: str = "",
    ) -> HackathonTeam | None:
        """Fetches team by team_name or team_id"""

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
    def update_team_query(
        cls, team_payload: Dict[str, Any],
        object_id: str,
    ) -> UpdateResult:
        query = {
            "$or": [
                {"_id": ObjectId(object_id)},
                {"team_name": team_payload.get("team_name")},
            ],
        }
        updated_team = t_col.find_one_and_update(
            query, {
                "$set": {
                    key: value for key, value in team_payload.items() if
                    value
                },
            }, projection={"_id": 0}, return_document=True,
        )

        return updated_team

    @classmethod
    def get_team_id_by_team_name(cls, team_name: str) -> str | None:
        if find_one_result := t_col.find_one(
                filter={"team_name": team_name},
        ):
            return str(find_one_result["_id"])
        return None

    @classmethod
    def generate_random_team_name(cls) -> str:
        count = t_col.count_documents({"team_name": "random"})
        return f"RandomTeam {count + 1}"

    @classmethod
    def add_team_to_db(cls, team: HackathonTeam) -> None:
        t_col.insert_one(team.model_dump())
