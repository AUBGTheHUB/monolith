from typing import Optional

from pymongo.asynchronous.client_session import AsyncClientSession
from result import Result, Ok, Err
from structlog.stdlib import get_logger
from bson import ObjectId
from pymongo import ReturnDocument

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
            candidate_form = await self._collection.find_one(
                filter={"_id": ObjectId(obj_id)}, projection={"_id": 0}, session=session
            )

            if candidate_form is None:
                return Err(CandidateFormNotFoundError())

            return Ok(CandidateForm(id=ObjectId(obj_id), **candidate_form))
        except Exception as e:
            LOG.exception("Failed to fetch candidate form due to error", candidate_form_id=obj_id, error=e)
            return Err(e)

    async def fetch_all(self, session: Optional[AsyncClientSession] = None) -> Result[list[CandidateForm], Exception]:
        try:
            LOG.info("Fetching all candidate forms")

            candidate_forms_data = await self._collection.find({}, session=session).to_list(length=None)
            candidate_forms: list[CandidateForm] = []

            for candidate_form in candidate_forms_data:
                candidate_form["id"] = candidate_form.pop("_id")

                candidate_forms.append(CandidateForm(**candidate_form))

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
                return Err(CandidateFormNotFoundError())

            return Ok(CandidateForm(id=ObjectId(obj_id), **result))

        except Exception as e:
            LOG.exception("Could not update candidate form", candidate_form_id=ObjectId(obj_id), error=e)
            return Err(e)

    async def delete(
        self, obj_id: str, session: Optional[AsyncClientSession] = None
    ) -> Result[CandidateForm, CandidateFormNotFoundError | Exception]:
        try:
            filter = {"_id": ObjectId(obj_id)}
            projection = {"_id": 0}
            result = await self._collection.find_one_and_delete(filter=filter, projection=projection, session=session)

            if result is None:
                return Err(CandidateFormNotFoundError())

            return Ok(CandidateForm(id=ObjectId(obj_id), **result))

        except Exception as e:
            LOG.exception("Candidate form deletion failed due to error", candidate_form_id=obj_id, error=e)
            return Err(e)

    async def create(
        self, candidate_form: CandidateForm, session: Optional[AsyncClientSession] = None
    ) -> Result[CandidateForm, CandidateFormNotFoundError | Exception]:
        try:
            LOG.info("Inserting candidate form...", candidate_form=candidate_form.dump_as_json())
            await self._collection.insert_one(document=candidate_form.dump_as_mongo_db_document(), session=session)
            return Ok(candidate_form)
        except Exception as e:
            LOG.debug("Candidate form insertion failed due to...", candidate_form_id=str(candidate_form.id), error=e)
            return Err(e)
