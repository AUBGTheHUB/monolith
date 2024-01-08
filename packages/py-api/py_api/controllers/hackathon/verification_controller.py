from fastapi.responses import JSONResponse
from py_api.functionality.hackathon.jwt_verification import JWTFunctionality


class VerificationController:
    @classmethod
    def verify_admin(cls, jwt_token: str) -> JSONResponse:
        try:
            decoded_token = JWTFunctionality.decode_token(jwt_token)
        except:
            return JSONResponse(status_code=401)

        # TODO: find team = PyMongo.find_one(decoded_token.get("team_name"))

        # if team:
        #     # switch the verified property of the team
        #     # and get the only participant within the team
        #     # and update its verified property too

        #     return {"message": "Team and admin were successfully verified"}

        # return JSONResponse(status_code=500, content={"message": "Something went wrong on our side"})
