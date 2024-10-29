from abc import ABC, abstractmethod
from typing import Dict, Any


class SerializableDbModel(ABC):
    @abstractmethod
    def dump_as_json(self) -> Dict[str, Any]:
        """This method should be used when returning an HTTP response"""
        raise NotImplementedError()

    @abstractmethod
    def dump_as_mongo_db_document(self) -> Dict[str, Any]:
        """This method should be used when constructing the document to be inserted/updated"""
        raise NotImplementedError()
