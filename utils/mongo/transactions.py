from typing import List

from models.core import Transaction
from utils.mongo import db

transactions = db["transactions"]


def add_transaction(transaction: Transaction):
    transactions.insert_one(transaction.to_dict())


def get_transactions_by_budget(budget_id: str) -> List[Transaction]:
    return [
        Transaction.from_dict(budget_data)
        for budget_data in transactions.find({"budget_id": budget_id})
    ]

