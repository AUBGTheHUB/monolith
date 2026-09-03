from result import is_err

from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.request_schemas.admin.candidates_form.question_schemas import (
    QuestionPostReqData,
    QuestionPatchReqData,
)
from src.server.schemas.response_schemas.admin.candidates_form.question_schemas import (
    QuestionResponse,
    QuestionsResponse,
)
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.candidates_form.questions_service import QuestionsService


# Questions Handlers
class QuestionsHandlers(BaseHandler):
    def __init__(self, service: QuestionsService) -> None:
        self._service = service

    async def create_question(self, request: QuestionPostReqData) -> Response:
        result = await self._service.create(
            prompt=request.prompt,
            question_type=request.question_type,
            answer_type=request.answer_type,
            options=request.options,
        )

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(QuestionResponse(question=result.ok_value), status_code=201)

    async def get_all_questions(self) -> Response:
        result = await self._service.get_all()

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(QuestionsResponse(questions=result.ok_value), status_code=200)

    async def get_question(self, object_id: str) -> Response:
        result = await self._service.get(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(QuestionResponse(question=result.ok_value), status_code=200)

    async def update_question(self, object_id: str, request: QuestionPatchReqData) -> Response:
        result = await self._service.update(
            question_id=object_id,
            prompt=request.prompt,
            question_type=request.question_type,
            answer_type=request.answer_type,
            answer=request.answer,
            options=request.options,
        )

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(QuestionResponse(question=result.ok_value), status_code=200)

    async def delete_question(self, object_id: str) -> Response:
        result = await self._service.delete(object_id)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(QuestionResponse(question=result.ok_value), status_code=200)
