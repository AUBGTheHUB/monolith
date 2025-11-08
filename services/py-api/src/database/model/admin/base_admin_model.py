from dataclasses import dataclass

from src.database.model.base_model import BaseDbModel, UpdateParams


@dataclass(kw_only=True)
class AdminBaseModel(BaseDbModel):
    """Common base for admin managed content."""


class AdminUpdateParams(UpdateParams):
    """Base update params for partial updates. Extend per entity as needed."""
