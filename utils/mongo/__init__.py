import pymongo

from config import MONGO_URL
from models.core import Singleton


class MongoBase(metaclass=Singleton):

    def __init__(self):
        db_client = pymongo.MongoClient(MONGO_URL)
        db = db_client["financier"]
        self.groups = db["groups"]
        self.budgets = db["budgets"]
        self.transactions = db["transactions"]
