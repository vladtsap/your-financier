from typing import List

from bson import ObjectId

from models.core import Budget, Transaction
from utils.mongo.core import MongoBase


class MongoBudgets(MongoBase):

    def add(self, budget: Budget):
        self.budgets.insert_one(budget.to_dict())

    def update_balance(self, transaction: Transaction, on_removing: bool = False):
        change = (-1 * transaction.outcome) if transaction.outcome else transaction.income

        if on_removing:
            change *= -1

        self.budgets.update_one(
            {"_id": ObjectId(transaction.budget_id)},
            {"$inc": {"left": change}}
        )

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

    def remove(self, budget_id: str):
        self.budgets.find_one_and_delete({"_id": ObjectId(budget_id)})

        # TODO: handle remove transactions on removing budgets
