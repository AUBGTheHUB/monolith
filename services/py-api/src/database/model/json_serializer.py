from abc import ABC, abstractmethod
from typing import Dict, Any


class SerializableDbModel(ABC):
    @abstractmethod
    def dump_as_json(self) -> Dict[str, Any]:
        """This method should be used when returning an HTTP response. When implementing it just return a dict mapping
        the obj fields to dict values. The id of the obj should be cast to string: "id": str(obj.id), otherwise an error
        will be prodcued when returning a response, as ObjectID is not json seriazable. (Thats why we need this method)
        """
        raise NotImplementedError()

    @abstractmethod
    def dump_as_mongo_db_document(self) -> Dict[str, Any]:
        """This method should be used when constructing the document to be inserted/updated in Mongo. When implementing
        it the id field of the db model should be mapped to a dcit key starting with an underscore as MongoDB expects it
        like this: "_id": obj.id.
        https://www.mongodb.com/docs/languages/python/pymongo-driver/current/write/insert/#the-_id-field"""
        raise NotImplementedError()
