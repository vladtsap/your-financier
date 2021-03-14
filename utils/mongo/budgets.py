from typing import List

from bson import ObjectId

from models.core import Budget, Transaction
from utils.mongo import db

budgets = db["budgets"]


def add_budget(budget: Budget):
    budgets.insert_one(budget.to_dict())


def get_budget_by_groups(group_ids: List[str]) -> List[Budget]:
    return [
        Budget.from_dict(budget_data)
        for budget_data in budgets.find({"group_id": {"$in": group_ids}})
    ]


def update_budget_balance(transaction: Transaction):
    change = (-1 * transaction.outcome) if transaction.outcome else transaction.income

    budgets.update_one({"_id": ObjectId(transaction.budget_id)}, {"$inc": {"left": change}})
