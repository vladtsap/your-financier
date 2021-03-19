from typing import List

from bson import ObjectId

from models.core import Budget, Transaction
from utils.mongo import MongoBase


class MongoBudgets(MongoBase):

    def add(self, budget: Budget):
        self.budgets.insert_one(budget.to_dict())

    def update_balance(self, transaction: Transaction):
        self.budgets.update_one(
            {"_id": ObjectId(transaction.budget_id)},
            {"$inc": {"left": (-1 * transaction.outcome) if transaction.outcome else transaction.income}}
        )

    def get_balance(self, budget: Budget):
        pass  # TODO

    def get_by_id(self, budget_id: str) -> Budget:
        if budget_content := self.budgets.find_one({"_id": ObjectId(budget_id)}):
            return Budget.from_dict(budget_content)
        else:
            return None  # TODO: raise exception

    def get_by_groups(self, group_ids: List[str]) -> List[Budget]:
        return [
            Budget.from_dict(budget_data)
            for budget_data in self.budgets.find({"group_id": {"$in": group_ids}})
        ]
