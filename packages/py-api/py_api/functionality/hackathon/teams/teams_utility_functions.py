from typing import Any, Dict, List, Optional

from bson import ObjectId
from py_api.database.initialize import t_col
from py_api.models import HackathonTeam
from py_api.models.hackathon_teams_models import TeamType
from pymongo.results import UpdateResult


class TeamFunctionality:

    @classmethod
    def create_team(
            cls, user_id: str,
            team_name: str | None = None, generate_random_team: bool = False,
    ) -> HackathonTeam | None:

        team_type = TeamType.NORMAL

        if generate_random_team:
            # Generate a team of type RANDOM for participants who are signing up themselves individually
            team_type = TeamType.RANDOM
            team_name = cls.generate_random_team_name()

        if cls.fetch_team(team_name=team_name):
            # Team with such name already exists
            return None

        # Upon team initialization, we need at least one team member who is considered the admin
        team_members_ids = [user_id]

        new_team = HackathonTeam(
            team_name=team_name,
            team_type=team_type, team_members=team_members_ids,
        )

        return new_team

    @classmethod
    def add_participant_to_team(
            cls, team_name: str,
            user_id: str,
    ) -> HackathonTeam | None:
        team = cls.fetch_team(team_name=team_name)

        if not team:
            raise Exception("Team doesn't exist")

        if len(team.team_members) == 6:
            raise Exception("Team is already at max capacity")

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
    def update_team_query(
            cls, team_payload: Dict[str, Any],
            object_id: str | None = None,
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
    def generate_random_team_name(cls) -> str:
        count = t_col.count_documents({"team_type": "random"})
        return f"RandomTeam {count + 1}"

    @classmethod
    def insert_team(cls, team: HackathonTeam) -> None:
        t_col.insert_one(team.model_dump())

    @classmethod
    def get_count_of_teams(cls) -> int:
        return int(t_col.count_documents({}))
