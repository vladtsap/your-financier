from datetime import datetime

from aiogram.types import Message

from config import dp
from models.core import Transaction
from utils import texts
from utils.mongo.budgets import MongoBudgets
from utils.mongo.groups import MongoGroups
from utils.mongo.transactions import MongoTransactions


@dp.message_handler(text=texts.ADD_TRANSACTION, state='*')
async def add_transaction_function(message: Message):
    for budget in MongoBudgets().get_by_groups([
        group.id for group in MongoGroups().get_by_member(message.from_user.id)
    ]):
        transaction = Transaction(
            budget_id=budget.id,
            member_id=message.from_user.id,
            date=datetime.now(),
            outcome=10,
        )

        MongoTransactions().add(transaction)
        MongoBudgets().update_balance(transaction)

    await message.answer(text='done')


@dp.message_handler(text=texts.VIEW_TRANSACTION, state='*')
async def get_transactions_function(message: Message):
    for budget in MongoBudgets().get_by_groups([
        group.id for group in MongoGroups().get_by_member(message.from_user.id)
    ]):
        for transaction in MongoTransactions().get_by_budget(budget.id):
            await message.answer(transaction.message_view)
