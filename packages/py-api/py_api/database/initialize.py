from os import getenv

from pymongo import MongoClient

# * How to use - https://pymongo.readthedocs.io/en/stable/tutorial.html
# e.g. db.jobs.find() where jobs is a collection in the database

# whenever you need to read from or write to the database
# you should import the db variable as follows:
# * from qb_api.database import db

client = MongoClient(getenv("MONGOURI"))
db = client["TheHubDB"]

# * use this collection when working within the UrlShortener controller
su_col = client["ShortenedUrlsDB"].shortened_urls
