import json
import random
import string
from typing import Any, Dict, List, Optional

from bson.json_util import dumps
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from py_api.database.initialize import t_col
from py_api.models import HackathonTeam
from py_api.models.hackathon_teams_models import (
    HackathonTeam,
    MoveTeamMembers,
    TeamType,
    UpdateTeam,
)
from py_api.utilities.parsers import filter_none_values


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
            team_members = members_list
            team_type = TeamType.RANDOM

        if cls.fetch_team(team_name):
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
            team_name=team_name,
            team_members=team["team_members"],
        )
        team.team_members.append(user_id)

        t_col.update_one(
            {"team_name": team.team_name}, {
                "$set": {"team_members": team.team_members},
            }, )

        return team.team_members

    @classmethod
    def fetch_team(cls, team_name: str = "", team_id: str = "") -> Dict[str, Any] | None:
        team: Dict[str, Any] = t_col.find_one(filter={"team_name": team_name})

        if team_id:
            team = t_col.find_one(filter={"_id": team_id})
            return team

        return team

    @staticmethod
    def fetch_teams() -> JSONResponse:
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

    @staticmethod
    def update_team(object_id: str, update_table_model: UpdateTeam) -> JSONResponse:
        fields_to_be_updated = filter_none_values(update_table_model)

        to_be_updated_team = t_col.find_one_and_update(
            {"_id": ObjectId(object_id)}, {
                "$set": fields_to_be_updated,
            },
            return_document=True,
        )

        if not to_be_updated_team:
            return JSONResponse(content={"message": "The team was not found"}, status_code=404)

        return JSONResponse(content={"teams": json.loads(dumps(to_be_updated_team))}, status_code=200)

    @classmethod
    def move_team_members(cls, move_members_model: MoveTeamMembers) -> JSONResponse:
        move_members_dump: Dict[str, Any] = move_members_model.model_dump()
        old_team_name = move_members_dump["old_team_name"]
        new_team_name = move_members_dump["new_team_name"]
        team_members_to_move = move_members_dump["team_members"]

        old_team = cls.fetch_team(old_team_name)
        if not old_team:
            return JSONResponse(
                content={
                    "message": f"The team {old_team_name} was not found, please check the spelling!",
                },
                status_code=404,
            )

        new_team = cls.fetch_team(new_team_name)
        if not new_team:
            cls.create_team(new_team_name, members_list=team_members_to_move)
            if content := cls.update_old_team_members_list(old_team, team_members_to_move):
                return JSONResponse(content={"message": content}, status_code=404)

            return JSONResponse(
                content={
                    "message": f"Created a new team with participants {team_members_to_move}",
                },
                status_code=201,
            )

        if content := cls.update_old_team_members_list(old_team, team_members_to_move):
            return JSONResponse(content={"message": content}, status_code=404)

        cls.update_new_team_members_list(new_team, team_members_to_move)

        return JSONResponse(
            content={
                "message": f"Team members {team_members_to_move} moved successfully from team {old_team_name}"
                           f" to team {new_team_name}",
            },
        )

    @classmethod
    def update_old_team_members_list(
            cls, old_team: Dict[str, Any],
            team_members_to_move: List[str],
    ) -> str | None:
        old_team_members: List[str] = old_team["team_members"]

        # Remove the passed team_members from their original team
        for team_member in team_members_to_move:
            if team_member in old_team_members:
                old_team_members.remove(team_member)
            else:
                return f"Team member with id {team_member} doesn't exist"

        cls.update_team_current_members(
            old_team["team_name"], old_team_members,
        )
        return None

    @classmethod
    def update_new_team_members_list(cls, new_team: Dict[str, Any], team_members_to_move: List[str]) -> None:
        new_team_current_members: List[str] = new_team["team_members"]

        # Add the passed team_members to the new team
        for new_team_member in team_members_to_move:
            new_team_current_members.append(new_team_member)

        cls.update_team_current_members(
            new_team["team_name"], new_team_current_members,
        )

    @classmethod
    def update_team_current_members(cls, team_name: str, members_list: List[str]) -> None:
        t_col.update_one(
            {"team_name": team_name}, {
                "$set": {"team_members": members_list},
            }, )

    @classmethod
    def generate_random_team_name(cls) -> str:
        count = t_col.count_documents({"team_name": "random"})
        return f"RandomTeam {count + 1}"
