import pymongo

from config import MONGO_URL

db_client = pymongo.MongoClient(MONGO_URL)
db = db_client["financier"]
