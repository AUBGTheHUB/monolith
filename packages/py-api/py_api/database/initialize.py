from os import getenv

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# How to use - https://pymongo.readthedocs.io/en/stable/tutorial.html
# e.g. db.jobs.find() where jobs is a collection in the database

# whenever you need to query the database or do any transcations
# you should import the db variable as follows:
# from qb_api.database import db

client = MongoClient(getenv("MONGOURI"))
db = client["TheHubDB"]
