from py_api.environment import MONGO_URI
from pymongo import MongoClient

# * How to use - https://pymongo.readthedocs.io/en/stable/tutorial.html
# e.g. db.jobs.find() where jobs is a collection in the database

# whenever you need to read from or write to the database
# you should import the db variable as follows:
# * from qb_api.database import db

client = MongoClient(MONGO_URI)
db = client["TheHubDB"]

# * use this collection when working within the UrlShortener controller
su_col = client["ShortenedUrlsDB"].shortened_urls

# * use these collections when working within the Questionnaire controller
q_col = client["questionnaires"].questions
a_col = client["questionnaires"].answers

# * use these collections when working within the Teams controller
t_col = client['hackathon'].normal_teams
