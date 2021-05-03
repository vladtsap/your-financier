from datetime import datetime, timedelta
from typing import List

from bson import ObjectId
from pytz import timezone

from models.core import Transaction
from utils.mongo.core import MongoBase


class MongoTransaction(MongoBase):

    def add(self, transaction: Transaction):
        self.transactions.insert_one(transaction.to_dict())

    def get_by_budget(self, budget_id: str) -> List[Transaction]:
        return [
            Transaction.from_dict(transaction_data)
            for transaction_data in self.transactions.find({"budget_id": budget_id})
        ]

    def get_all_for_today_by_budget(self, budget_id: str) -> List[Transaction]:
        if not budget_id:
            pass  # TODO: raise exception

        today = datetime.now(timezone('Europe/Kiev'))
        start = datetime(today.year, today.month, today.day)
        end = start + timedelta(days=1)

        return [
            Transaction.from_dict(transaction_data)
            for transaction_data in self.transactions.find({
                "budget_id": budget_id,
                "date": {
                    "$gte": start.isoformat(),
                    "$lt": end.isoformat(),
                }
            })
        ]

    def remove(self, transaction_id: str) -> Transaction:
        if transaction_content := self.transactions.find_one_and_delete({"_id": ObjectId(transaction_id)}):
            return Transaction.from_dict(transaction_content)
        else:
            return None  # TODO: raise exception

    def remove_all_in_budget(self, budget_id: str):
        self.transactions.delete_many({"budget_id": budget_id})
