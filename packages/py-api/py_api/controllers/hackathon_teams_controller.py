import json
from typing import Any, Dict, List, Optional, Set

from bson.json_util import dumps
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from py_api.database.initialize import t_col
from py_api.models.hackathon_teams_models import (
    HackathonTeam,
    MoveTeamMembers,
    TeamType,
    UpdateTeam,
)
from py_api.utilities.parsers import filter_none_values
from pymongo.results import UpdateResult


class TeamsController:
    @classmethod
    def create_team(
            cls, team_name: str, user_id: str = "",
            members_list: Optional[List[str]] = None,
    ) -> HackathonTeam | None:
        team_type = TeamType.NORMAL

        if not team_name:
            # If no team_name is provided during registration, the participant is registering individually.
            # We create a team of type RANDOM which should be filled with such participants
            team_type = TeamType.RANDOM
            team_name = cls.generate_random_team_name()

        team_members = []

        if user_id:
            team_members = [user_id]

        if members_list:
            team_members = list(members_list)
            # Assumes that we are creating a random team when moving members from existing team to a non-existing one
            team_type = TeamType.RANDOM

        if cls.fetch_team(team_name):
            # A name with this team_name exist so no new team is created
            return None

        new_team = HackathonTeam(
            team_name=team_name,
            team_type=team_type, team_members=team_members,
        )
        t_col.insert_one(new_team.model_dump())

        return new_team

    @classmethod
    def add_team_participant(cls, team_name: str, user_id: str) -> List[str] | None:
        team = cls.fetch_team(team_name=team_name)
        if not team:
            return None

        team = HackathonTeam(
            team_name=team_name, team_members=team["team_members"], team_type=team["team_type"],
        )
        team.team_members.append(user_id)

        cls.update_team_fields(team)

        return team.team_members

    @classmethod
    def fetch_team(cls, team_name: str = "", team_id: str = "") -> Dict[str, Any]:
        team: Dict[str, Any] = t_col.find_one(filter={"team_name": team_name})

        if team_id:
            team = t_col.find_one(filter={"_id": ObjectId(team_id)})
            return team

        return team

    @classmethod
    def fetch_teams(cls) -> JSONResponse:
        teams = list(t_col.find())

        if not teams:
            return JSONResponse(content={"message": "No teams were found in db"}, status_code=404)

        return JSONResponse(content={"teams": json.loads(dumps(teams))}, status_code=200)

    @classmethod
    def get_team(cls, object_id: str) -> JSONResponse:
        specified_team = cls.fetch_team(team_id=object_id)

        if not specified_team:
            return JSONResponse(content={"message": "The team was not found"}, status_code=404)

        return JSONResponse(content={"participant": json.loads(dumps(specified_team))}, status_code=200)

    @staticmethod
    def delete_team(object_id: str) -> JSONResponse:
        delete_team = t_col.find_one_and_delete(
            filter={"_id": ObjectId(object_id)},
        )

        if not delete_team:
            return JSONResponse(content={"message": "The team was not found"}, status_code=404)

        return JSONResponse(content={"message": json.loads(dumps(delete_team))}, status_code=200)

    @staticmethod
    def team_count() -> JSONResponse:
        count = t_col.count_documents({})

        if not count:
            return JSONResponse(content={"message": "No teams were found"}, status_code=404)

        return JSONResponse(content={"teams": count})

    @classmethod
    def update_team(cls, object_id: str, update_table_model: UpdateTeam) -> JSONResponse:
        team = cls.fetch_team(team_id=object_id)

        if not team:
            return JSONResponse(content={"message": "The team was not found"}, status_code=404)

        result = cls.update_team_fields(
            update_table_model, object_id=object_id,
        )

        return JSONResponse(content={"teams": json.loads(dumps(result))}, status_code=200)

    @classmethod
    def move_team_members(cls, move_members_model: MoveTeamMembers) -> JSONResponse:
        move_members_dump: Dict[str, Any] = move_members_model.model_dump()
        from_team: str = move_members_dump["from_team"]
        target_team: str = move_members_dump["to_team"]
        team_members_to_move: List[str] = list(
            set(move_members_dump["team_members"]),
        )

        from_team_obj = cls.fetch_team(team_name=from_team)
        if not from_team_obj:
            return JSONResponse(
                content={
                    "message": f"The team {from_team} was not found, please check the spelling!",
                },
                status_code=404,
            )

        if cls.create_team(team_name=target_team, members_list=team_members_to_move):

            if error := cls.update_members_for_from_team(from_team_obj, team_members_to_move):
                return JSONResponse(content={"message": error}, status_code=404)

            return JSONResponse(
                content={
                    "message": f"Created a new team {target_team} with participants {team_members_to_move}",
                },
                status_code=201,
            )

        if error := cls.update_members_for_from_team(from_team_obj, team_members_to_move):
            return JSONResponse(content={"message": error}, status_code=404)

        cls.update_members_for_target_team(
            cls.fetch_team(team_name=target_team), team_members_to_move,
        )

        return JSONResponse(
            content={
                "message": f"Team members {team_members_to_move} moved successfully from team {from_team}"
                           f" to team {target_team}",
            },
        )

    @classmethod
    def update_members_for_from_team(cls, from_team: Dict[str, Any], team_members_to_move: List[str]) -> str | None:
        from_team_current_members: List[str] = from_team["team_members"]
        # Remove the passed team_members from their original team
        for team_member in team_members_to_move:
            if team_member in from_team_current_members:
                from_team_current_members.remove(team_member)
            else:
                return f"Team member with id {team_member} doesn't exist"

        update_team_obj = HackathonTeam(
            team_name=from_team["team_name"], team_members=from_team_current_members,
            team_type=from_team["team_type"],
        )
        cls.update_team_fields(update_team_obj)

        return None

    @classmethod
    def update_members_for_target_team(cls, target_team: Dict[str, Any], team_members_to_move: List[str]) -> None:
        target_team_current_members: List[str] = target_team["team_members"]

        # Add the passed team_members to the new team
        target_team_current_members.extend(team_members_to_move)

        target_team_obj = HackathonTeam(
            team_name=target_team["team_name"], team_members=target_team_current_members,
            team_type=target_team["team_type"],
        )
        cls.update_team_fields(target_team_obj)

    @classmethod
    def update_team_fields(cls, update_model: UpdateTeam | HackathonTeam, object_id: str = "") -> UpdateResult:
        if isinstance(update_model, UpdateTeam):
            fields_to_be_updated = filter_none_values(update_model)
        else:
            fields_to_be_updated = update_model.model_dump()

        if object_id:
            updated_team = t_col.find_one_and_update(
                {"_id": ObjectId(object_id)}, {
                    "$set": fields_to_be_updated,
                }, return_document=True,
            )
        else:
            updated_team = t_col.find_one_and_update(
                {"team_name": update_model.team_name}, {
                    "$set": fields_to_be_updated,
                }, return_document=True,
            )

        return updated_team

    @classmethod
    def generate_random_team_name(cls) -> str:
        count = t_col.count_documents({"team_name": "random"})
        return f"RandomTeam {count + 1}"
