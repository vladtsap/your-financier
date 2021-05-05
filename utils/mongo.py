from datetime import datetime, timedelta
from typing import List

import pymongo
from bson import ObjectId
from pytz import timezone

from config import MONGO_URL
from models.core import Singleton, Group, Budget, Transaction


class MongoBase(metaclass=Singleton):

    def __init__(self):
        db_client = pymongo.MongoClient(MONGO_URL)
        db = db_client["financier"]
        self.groups = db["groups"]
        self.budgets = db["budgets"]
        self.transactions = db["transactions"]


class MongoGroup(MongoBase):

    def add(self, group: Group):
        return self.groups.insert_one(group.to_dict()).inserted_id

    def add_member(self, group: Group, member_id: int):
        self.groups.update_one(
            {"_id": ObjectId(group.id)},
            {"$addToSet": {"members": member_id}},
        )

    def is_new(self, member_id: int) -> bool:
        return not bool(list(self.groups.find(
            {'members': [member_id]}  # TODO: add check for name too?
        )))

    def get_by_id(self, group_id: str) -> Group:
        if group_content := self.groups.find_one({"_id": ObjectId(group_id)}):
            return Group.from_dict(group_content)
        else:
            return None  # TODO: raise exception

    def get_by_member(self, member_id: int) -> List[Group]:
        return [
            Group.from_dict(group_content)
            for group_content in self.groups.find({"members": member_id})
        ]

    def get_by_name(self, name: str) -> Group:
        if group_content := self.groups.find_one({"name": name}):
            return Group.from_dict(group_content)
        else:
            return None  # TODO: raise exception


class MongoBudget(MongoBase):

    def add(self, budget: Budget):
        return self.budgets.insert_one(budget.to_dict()).inserted_id

    def update_balance(self, transaction: Transaction, on_removing: bool = False):
        change = (-1 * transaction.outcome) if transaction.outcome else transaction.income

        if on_removing:
            change *= -1

        return self.budgets.update_one(
            {"_id": ObjectId(transaction.budget_id)},
            {"$inc": {"left": change}}
        ).upserted_id

    def get_by_id(self, budget_id: str) -> Budget:
        if budget_content := self.budgets.find_one({"_id": ObjectId(budget_id)}):
            return Budget.from_dict(budget_content)
        else:
            return None  # TODO: raise exception

    def get_by_name(self, name: str) -> Budget:
        if budget_content := self.budgets.find_one({"name": name}):
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
        MongoTransaction().remove_all_in_budget(budget_id)


class MongoTransaction(MongoBase):

    def add(self, transaction: Transaction):
        MongoBudget().update_balance(transaction)
        return self.transactions.insert_one(transaction.to_dict()).inserted_id

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
            MongoBudget().update_balance(
                transaction := Transaction.from_dict(transaction_content),
                on_removing=True
            )
            return transaction
        else:
            return None  # TODO: raise exception

    def remove_all_in_budget(self, budget_id: str):
        self.transactions.delete_many({"budget_id": budget_id})
