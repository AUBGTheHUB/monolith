import json
import random
import string
from enum import Enum
from typing import Any, Dict, List

from bson.json_util import dumps
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from py_api.database.initialize import t_col
from py_api.models.hackathon_teams_models import (
    HackathonTeam,
    MoveTeamMembers,
    UpdateTeam,
)
from py_api.utilities.parsers import filter_none_values


class TeamType(Enum):
    NORMAL = "normal"
    RANDOM = "random"


class TeamsController:
    @classmethod
    def create_team(cls, team_name: str, user_id: str) -> Dict[str, Any] | None:
        team_type = TeamType.NORMAL

        if not team_name:
            # If no team_name is provided during registration, the participant is registering individually.
            # We create a team of type RANDOM which should be filled with such participants

            team_name = ''.join(
                random.choice(string.ascii_letters)
                for _ in range(8)
            )
            team_type = TeamType.RANDOM

        team = cls.check_if_team_exists(team_name)

        if not team:
            new_team = HackathonTeam(
                team_name=team_name,
                team_type=team_type, team_members=[user_id],
            )
            t_col.insert_one(new_team.model_dump())

            return None

        return team

    @classmethod
    def add_team_participant(cls, team_name: str, user_id: str) -> List[str] | None:
        team = cls.check_if_team_exists(team_name)

        if not team:
            return None

        team_members: List[str] = team["team_members"]
        team_members.append(user_id)

        t_col.update_one(
            {"team_name": team_name}, {
                "$set": {"team_members": team_members},
            }, )

        return team_members

    @classmethod
    def check_if_team_exists(cls, team_name: str) -> Dict[str, Any] | None:
        team: Dict[str, Any] = t_col.find_one(filter={"team_name": team_name})
        return team

    @staticmethod
    def fetch_teams() -> JSONResponse:
        teams = list(t_col.find())

        if not teams:
            return JSONResponse(content={"message": "No teams were found in db"}, status_code=404)

        return JSONResponse(content={"teams": json.loads(dumps(teams))}, status_code=200)

    @staticmethod
    def get_team(object_id: str) -> JSONResponse:
        specified_team = t_col.find_one(filter={"_id": ObjectId(object_id)})

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

        if not cls.check_if_team_exists(old_team_name):
            return JSONResponse(
                content={
                    "message": f"The team {old_team_name} was not found, please check the spelling!",
                },
                status_code=404,
            )

        if not cls.check_if_team_exists(new_team_name):
            pass
