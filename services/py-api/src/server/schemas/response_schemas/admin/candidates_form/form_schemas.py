from typing import Any

from pydantic import BaseModel, ConfigDict, field_serializer

from src.database.model.admin.candidates_form.form_model import CandidateForm


class CandidateFormResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    candidate_form: CandidateForm

    @field_serializer("candidate_form")
    def serialize_form(self, candidate_form: CandidateForm) -> dict[str, Any]:
        return candidate_form.dump_as_json()


class CandidateFormsResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    candidate_forms: list[CandidateForm]

    @field_serializer("candidate_forms")
    def serialize_form(self, candidate_forms: list[CandidateForm]) -> list[dict[str, Any]]:
        return [candidate_form.dump_as_json() for candidate_form in candidate_forms]
