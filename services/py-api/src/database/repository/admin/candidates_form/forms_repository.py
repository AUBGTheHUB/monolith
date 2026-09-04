from typing import Optional

from pymongo.asynchronous.client_session import AsyncClientSession
from result import Result, Ok, Err
from structlog.stdlib import get_logger
from bson import ObjectId
from pymongo import ReturnDocument

from src.database.model.admin.candidates_form.question_model import Question
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.mongo.collections.admin_collections import CANDIDATES_FORMS_COLLECTION
from src.database.model.admin.candidates_form.form_model import CandidateForm, UpdateCandidateFormParams
from src.database.repository.base_repository import CRUDRepository
from src.exception import CandidateFormNotFoundError

LOG = get_logger()


class CandidateFormsRepository(CRUDRepository[CandidateForm]):
    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(CANDIDATES_FORMS_COLLECTION)

    async def fetch_by_id(
        self, obj_id: str, session: Optional[AsyncClientSession] = None
    ) -> Result[CandidateForm, CandidateFormNotFoundError | Exception]:
        try:
            LOG.info("Fetching candidate form by ObjectId", candidate_form_id=obj_id)

            # Query the db for the candidate_form with the given id
            candidate_form = await self._collection.find_one(filter={"_id": ObjectId(obj_id)}, session=session)

            if candidate_form is None:
                return Err(CandidateFormNotFoundError())

            return Ok(CandidateForm.from_mongo_db_document(candidate_form))
        except Exception as e:
            LOG.exception("Failed to fetch candidate form due to error", candidate_form_id=obj_id, error=e)
            return Err(e)

    async def fetch_all(self, session: Optional[AsyncClientSession] = None) -> Result[list[CandidateForm], Exception]:
        try:
            LOG.info("Fetching all candidate forms")

            candidate_forms_data = await self._collection.find({}, session=session).to_list(length=None)
            candidate_forms: list[CandidateForm] = [
                CandidateForm.from_mongo_db_document(document) for document in candidate_forms_data
            ]

            LOG.debug("Result", result=candidate_forms)

            LOG.debug(f"Fetched {len(candidate_forms)} candidate forms.")
            return Ok(candidate_forms)

        except Exception as e:
            LOG.exception(f"Failed to fetch all candidate forms due to err: {e}")
            return Err(e)

    async def update(
        self, obj_id: str, obj_fields: UpdateCandidateFormParams, session: Optional[AsyncClientSession] = None
    ) -> Result[CandidateForm, CandidateFormNotFoundError | Exception]:
        try:
            filter = {"_id": ObjectId(obj_id)}

            update_data = obj_fields.model_dump(
                exclude_none=True,
                exclude_unset=True,
            )

            if obj_fields.questions is not None:
                questions = [
                    Question(
                        prompt=question.prompt,
                        options=question.options,
                        answer=question.answer,
                        question_type=question.question_type,
                        answer_type=question.answer_type,
                    )
                    for question in obj_fields.questions
                ]

                update_data["questions"] = [question.dump_as_mongo_db_document() for question in questions]

            update = {"$set": update_data}

            # ReturnDocument.AFTER returns the updated document with the new data
            result = await self._collection.find_one_and_update(
                filter=filter,
                update=update,
                return_document=ReturnDocument.AFTER,
                session=session,
            )

            if result is None:
                return Err(CandidateFormNotFoundError())

            return Ok(CandidateForm.from_mongo_db_document(result))

        except Exception as e:
            LOG.exception("Could not update candidate form", candidate_form_id=ObjectId(obj_id), error=e)
            return Err(e)

    async def delete(
        self, obj_id: str, session: Optional[AsyncClientSession] = None
    ) -> Result[CandidateForm, CandidateFormNotFoundError | Exception]:
        try:
            filter = {"_id": ObjectId(obj_id)}
            result = await self._collection.find_one_and_delete(filter=filter, session=session)

            LOG.debug("Result", result=result)
            LOG.debug("Type", type=type(result))

            if result is None:
                return Err(CandidateFormNotFoundError())

            return Ok(CandidateForm.from_mongo_db_document(result))

        except Exception as e:
            LOG.exception("Candidate form deletion failed due to error", candidate_form_id=obj_id, error=e)
            return Err(e)

    async def create(
        self, obj: CandidateForm, session: Optional[AsyncClientSession] = None
    ) -> Result[CandidateForm, CandidateFormNotFoundError | Exception]:
        try:
            LOG.info("Inserting candidate form...", candidate_form=obj.dump_as_json())
            await self._collection.insert_one(document=obj.dump_as_mongo_db_document(), session=session)
            return Ok(obj)
        except Exception as e:
            LOG.debug("Candidate form insertion failed due to...", candidate_form_id=str(obj.id), error=e)
            return Err(e)
