from typing import Optional

from pymongo.asynchronous.client_session import AsyncClientSession
from result import Result, Ok, Err
from structlog.stdlib import get_logger
from bson import ObjectId
from pymongo import ReturnDocument

from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.mongo.collections.admin_collections import CANDIDATES_FORM_QUESTIONS_COLLECTION
from src.database.model.admin.candidates_form.question_model import Question, UpdateQuestionParams
from src.database.repository.base_repository import CRUDRepository
from src.exception import QuestionNotFoundError

LOG = get_logger()


class QuestionsRepository(CRUDRepository[Question]):
    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(CANDIDATES_FORM_QUESTIONS_COLLECTION)

    async def fetch_by_id(
        self, obj_id: str, session: Optional[AsyncClientSession] = None
    ) -> Result[Question, QuestionNotFoundError | Exception]:
        try:
            LOG.info("Fetching question by ObjectId", question_id=obj_id)

            # Query the db for the question with the given id
            question = await self._collection.find_one(
                filter={"_id": ObjectId(obj_id)}, projection={"_id": 0}, session=session
            )

            if question is None:
                return Err(QuestionNotFoundError())

            return Ok(Question(id=ObjectId(obj_id), **question))
        except Exception as e:
            LOG.exception("Failed to fetch question due to error", question_id=obj_id, error=e)
            return Err(e)

    async def fetch_all(self, session: Optional[AsyncClientSession] = None) -> Result[list[Question], Exception]:
        try:
            LOG.info("Fetching all questions")

            questions_data = await self._collection.find({}, session=session).to_list(length=None)
            questions: list[Question] = []

            for question in questions_data:
                question["id"] = question.pop("_id")

                questions.append(Question(**question))

            LOG.debug(f"Fetched {len(questions)} questions.")
            return Ok(questions)

        except Exception as e:
            LOG.exception(f"Failed to fetch all questions due to err: {e}")
            return Err(e)

    async def update(
        self, obj_id: str, obj_fields: UpdateQuestionParams, session: Optional[AsyncClientSession] = None
    ) -> Result[Question, QuestionNotFoundError | Exception]:
        try:
            filter = {"_id": ObjectId(obj_id)}
            update = {"$set": obj_fields.model_dump(exclude_none=True, exclude_unset=True)}
            projection = {"_id": 0}

            # ReturnDocument.AFTER returns the updated document with the new data
            result = await self._collection.find_one_and_update(
                filter=filter,
                update=update,
                projection=projection,
                return_document=ReturnDocument.AFTER,
                session=session,
            )

            if result is None:
                return Err(QuestionNotFoundError())

            return Ok(Question(id=ObjectId(obj_id), **result))

        except Exception as e:
            LOG.exception("Could not update question", question_id=ObjectId(obj_id), error=e)
            return Err(e)

    async def delete(
        self, obj_id: str, session: Optional[AsyncClientSession] = None
    ) -> Result[Question, QuestionNotFoundError | Exception]:
        try:
            filter = {"_id": ObjectId(obj_id)}
            projection = {"_id": 0}
            result = await self._collection.find_one_and_delete(filter=filter, projection=projection, session=session)

            if result is None:
                return Err(QuestionNotFoundError())

            return Ok(Question(id=ObjectId(obj_id), **result))

        except Exception as e:
            LOG.exception("Question deletion failed due to error", question_id=obj_id, error=e)
            return Err(e)

    async def create(
        self, question: Question, session: Optional[AsyncClientSession] = None
    ) -> Result[Question, QuestionNotFoundError | Exception]:
        try:
            LOG.info("Inserting question...", question=question.dump_as_json())
            await self._collection.insert_one(document=question.dump_as_mongo_db_document(), session=session)
            return Ok(question)
        except Exception as e:
            LOG.debug("Question insertion failed due to...", question_id=str(question.id), error=e)
            return Err(e)
