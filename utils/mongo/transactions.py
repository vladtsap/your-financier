from typing import List

from models.core import Transaction
from utils.mongo import MongoBase


class MongoTransactions(MongoBase):

    def add(self, transaction: Transaction):
        self.transactions.insert_one(transaction.to_dict())

    def get_by_budget(self, budget_id: str) -> List[Transaction]:
        return [
            Transaction.from_dict(budget_data)
            for budget_data in self.transactions.find({"budget_id": budget_id})
        ]
