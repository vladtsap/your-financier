from datetime import datetime

from aiogram.types import Message

from config import dp
from models.core import Transaction
from utils.mongo.budgets import get_budget_by_groups, update_budget_balance
from utils.mongo.groups import get_groups_by_member
from utils.mongo.transactions import add_transaction, get_transactions_by_budget


@dp.message_handler(state='*', commands=['add_transaction'])
async def add_transaction_function(message: Message):
    for budget in get_budget_by_groups([
        group.id for group in get_groups_by_member(message.from_user.id)
    ]):
        transaction = Transaction(
            budget_id=budget.id,
            member_id=message.from_user.id,
            date=datetime.now(),
            outcome=10,
        )

        add_transaction(transaction)
        update_budget_balance(transaction)

    await message.answer(text='done')


@dp.message_handler(state='*', commands=['get_transactions'])
async def get_transactions_function(message: Message):
    for budget in get_budget_by_groups([
        group.id for group in get_groups_by_member(message.from_user.id)
    ]):
        for transaction in get_transactions_by_budget(budget.id):
            await message.answer(str(transaction.to_dict()))
