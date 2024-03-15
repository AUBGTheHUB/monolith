import json

import pandas as pd
from bson.json_util import dumps
from bson.objectid import ObjectId
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from pandas import DataFrame
from py_api.database.initialize import participants_col, t_col
from py_api.functionality.hackathon.teams_base import TeamFunctionality
from py_api.models.hackathon_teams_models import HackathonTeam, UpdateTeam


class TeamsController:

    @classmethod
    def fetch_teams(cls) -> JSONResponse:
        teams = list(t_col.find())

        if not teams:
            return JSONResponse(
                content={"message": "No teams were found in db"},
                status_code=404,
            )

        return JSONResponse(
            content={"teams": json.loads(dumps(teams))},
            status_code=200,
        )

    @classmethod
    def get_team(cls, object_id: str) -> JSONResponse:
        specified_team = TeamFunctionality.fetch_team(team_id=object_id)
        if not specified_team:
            return JSONResponse(
                content={"message": "The team was not found"},
                status_code=404,
            )

        return JSONResponse(
            content={"team": specified_team.model_dump()},
            status_code=200,
        )

    @staticmethod
    def delete_team(object_id: str) -> JSONResponse:
        delete_team = TeamFunctionality.delete_team(object_id)
        # delete all participants from the team
        if not delete_team:
            return JSONResponse(
                content={"message": "The team was not found"},
                status_code=404,
            )

        return JSONResponse(
            content={"message": json.loads(dumps(delete_team))},
            status_code=200,
        )

    @staticmethod
    def team_count() -> JSONResponse:
        count = TeamFunctionality.get_count_of_teams()

        if count == 0:
            return JSONResponse(
                content={"message": "No teams were found"},
                status_code=404,
            )

        return JSONResponse(content={"teams": count})

    @classmethod
    def update_team(
        cls, object_id: str,
        team_payload: UpdateTeam | HackathonTeam,
    ) -> JSONResponse:

        updated_team = TeamFunctionality.update_team_query_using_dump(
            team_payload=team_payload.model_dump(), object_id=object_id,
        )

        if not updated_team:
            return JSONResponse(
                content={"message": "The team was not found"},
                status_code=404,
            )

        return JSONResponse(content={"team": updated_team.model_dump()}, status_code=200)

    @classmethod
    def get_teams(cls) -> JSONResponse:
        teams = list(t_col.find())

        if not teams:
            return JSONResponse(
                content={"message": "No teams were found in db"},
                status_code=404,
            )

        # Create a new Excel workbook
        wb = Workbook()

        for i, team in enumerate(teams):
            team_members = []
            team.pop('_id', None)
            team.pop('team_type', None)
            team['TeamName'] = team.pop('team_name', None)
            team['IsTeamVerified'] = team.pop('is_verified', None)

            for member_id in team["team_members"]:
                participant = participants_col.find_one(
                    {"_id": ObjectId(member_id)},
                )
                if participant:
                    participant.pop('_id', None)
                    participant.pop('team_name', None)
                    participant['First Name'] = participant.pop(
                        'first_name', None,
                    )
                    participant['Last Name'] = participant.pop(
                        'last_name', None,
                    )
                    participant['Age'] = participant.pop('age', None)
                    participant['Location'] = participant.pop('location', None)
                    participant['University'] = participant.pop(
                        'university', None,
                    )
                    participant['Tshirt Size'] = participant.pop(
                        'tshirt_size', None,
                    )
                    participant['Source of referral'] = participant.pop(
                        'source_of_referral', None,
                    )
                    participant['Programming Language'] = participant.pop(
                        'programming_language', None,
                    )
                    participant['Programming Level'] = participant.pop(
                        'programming_level', None,
                    )
                    participant['Prev HackAUBG Participation'] = participant.pop(
                        'has_participated_in_hackaubg', None,
                    )
                    participant['Internship'] = participant.pop(
                        'has_internship_interest', None,
                    )
                    participant['Participation in other hackathons'] = participant.pop(
                        'has_participated_in_hackathons', None,
                    )
                    participant['Prev Experience'] = participant.pop(
                        'has_previous_coding_experience', None,
                    )
                    participant['Share with sponsors'] = participant.pop(
                        'share_info_with_sponsors', None,
                    )
                    participant['IsAdmin'] = participant.pop('is_admin', None)
                    participant['IsVerified'] = participant.pop(
                        'is_verified', None,
                    )

                    team_members.append(participant)
            team["team_members"] = team_members

            df = DataFrame([team])
            df = df.apply(
                lambda x: x.explode() if x.name ==
                'team_members' else x,
            )
            df = pd.json_normalize(df.to_dict(orient='records'))
            df.columns = df.columns.str.replace('team_members.', '')

            if i == 0:
                sheet = wb.active
                sheet.title = team['TeamName']
            else:
                sheet = wb.create_sheet(title=team['TeamName'])

            for r in dataframe_to_rows(df, index=False, header=True):
                sheet.append(r)

        file_name = 'teams.xlsx'
        wb.save(file_name)

        return FileResponse(file_name, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=file_name)
