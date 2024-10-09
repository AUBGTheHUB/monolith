from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from src.server.handlers.main_handlers import MainHandlers
from src.server.schemas.request_schemas.schemas import RequestBody
from src.server.schemas.response_schemas.schemas import ErrResponse, EmailSentResponse

main_router = APIRouter()


@main_router.post("/send", responses={202: {"model": EmailSentResponse}, 500: {"model": ErrResponse}})
async def send_email(req_body: RequestBody, response: Response) -> EmailSentResponse | ErrResponse:
    err = await MainHandlers.send_mail(req_body.receiver, req_body.subject, req_body.body)
    if err:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrResponse(error=f"Sending of email to {req_body.receiver} failed!")

    response.status_code = status.HTTP_202_ACCEPTED
    return EmailSentResponse(message=f"Email successfully sent to {req_body.receiver}")
