from typing import Dict, List

from py_api.database import su_col


class UrlShortenerController:

    @classmethod
    def fetch_shortened_urls(cls) -> Dict[str, List[Dict[str, str]]]:
        projection = {"_id": 0}
        cursor = su_col.find({}, projection)
        shortened_urls = [doc for doc in cursor]

        return {"urls": shortened_urls}

    @classmethod
    def delete_shortened_url(cls, endpoint: str) -> Dict[str, str]:
        return {"message": "Endpoint has been deleted!"}

    @classmethod
    def upsert_shortened_url(cls, endpoint: str) -> Dict[str, str]:
        return {"message": "Shortened url has been successfully created/updated!"}
