from typing import Dict, Tuple

import jwt
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from py_api.database.initialize import participants_col
from py_api.environment import SECRET_KEY


class VerificationController:
    @classmethod
    def invite(cls) -> JSONResponse:
        # TODO:
        #  - Check the cap of the team
        #  - If cap reached -> return proper message
        #  - Else insert a new participant document and add the inserted
        #  Object id to the list of paticipnats ids for the provided team (team_name from jwt)
        pass

    @classmethod
    def verify(cls) -> JSONResponse:
        # This is when a participant is registering (Either with a team or without one)
        # TODO:
        #   - 1. Check the result of the verify_participant
        #   - 2. Get the team_name from the jwt
        #   - 3. Based on it use the functions in py_api/functionality/hackathon/teams/teams_utility_functions.py to create a team
        #   You can look at a sample code snippet in the ad_participant func in py_api/controllers/hackathon_participants_controller.py
        pass
