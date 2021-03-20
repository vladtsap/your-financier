from typing import List

from bson import ObjectId

from models.core import Transaction
from utils.mongo.core import MongoBase


class MongoTransactions(MongoBase):

    def add(self, transaction: Transaction):
        self.transactions.insert_one(transaction.to_dict())

    def get_by_budget(self, budget_id: str) -> List[Transaction]:
        return [
            Transaction.from_dict(budget_data)
            for budget_data in self.transactions.find({"budget_id": budget_id})
        ]

    def remove(self, transaction_id: str) -> Transaction:
        if transaction_content := self.transactions.find_one_and_delete({"_id": ObjectId(transaction_id)}):
            return Transaction.from_dict(transaction_content)
        else:
            return None  # TODO: raise exception
