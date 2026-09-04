from result import is_err

from src.database.model.admin.candidates_form.question_model import Question
from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.request_schemas.admin.candidates_form.form_schemas import (
    CandidateFormPostReqData,
    CandidateFormPatchReqData,
)
from src.server.schemas.response_schemas.admin.candidates_form.form_schemas import (
    CandidateFormResponse,
    CandidateFormsResponse,
)
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.candidates_form.forms_service import CandidateFormsService


# Candidate Forms Handlers
class CandidateFormsHandlers(BaseHandler):
    def __init__(self, service: CandidateFormsService) -> None:
        self._service = service

    async def create_form(self, request: CandidateFormPostReqData) -> Response:
        result = await self._service.create(
            questions=[
                Question(
                    prompt=question.prompt,
                    answer=question.answer,
                    question_type=question.question_type,
                    answer_type=question.answer_type,
                    options=question.options,
                )
                for question in request.questions
            ]
        )

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(CandidateFormResponse(candidate_form=result.ok_value), status_code=201)

    async def get_all_forms(self) -> Response:
        result = await self._service.get_all()

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(CandidateFormsResponse(candidate_forms=result.ok_value), status_code=200)

    async def get_form(self, object_id: str) -> Response:
        result = await self._service.get(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(CandidateFormResponse(candidate_form=result.ok_value), status_code=200)

    async def update_form(self, object_id: str, request: CandidateFormPatchReqData) -> Response:
        result = await self._service.update(candidate_form_id=object_id, questions=request.questions)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(CandidateFormResponse(candidate_form=result.ok_value), status_code=200)

    async def delete_form(self, object_id: str) -> Response:
        result = await self._service.delete(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(CandidateFormResponse(candidate_form=result.ok_value), status_code=200)
