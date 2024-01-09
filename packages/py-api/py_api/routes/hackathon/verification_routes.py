from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from py_api.controllers.hackathon.verification_controller import (
    VerificationController as c,
)

router = APIRouter(prefix="/hackathon/verify")


@router.get("/admin")
def verify_admin(jwt_token: str) -> JSONResponse:
    return c.verify_admin(jwt_token)


# @router.get("/test")
# def verify_url(jwt_token: str, is_frontend: bool, request: Request) -> JSONResponse:
#     return {'url': JWTFunctionality.get_verification_link(jwt_token, domain=get_hostname_with_protocol(request), for_frontend=is_frontend)}
