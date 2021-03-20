from datetime import datetime

from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from config import dp, bot
from keyboards.inline import transaction_keyboard
from models import callbacks
from models.core import Transaction
from utils import texts
from utils.mongo import (
    MongoGroups,
    MongoBudgets,
    MongoTransactions,
)


@dp.message_handler(text=texts.ADD_TRANSACTION, state='*')
async def add_transaction_function(message: Message):
    budgets = MongoBudgets()
    for budget in budgets.get_by_groups([
        group.id for group in MongoGroups().get_by_member(message.from_user.id)
    ]):
        transaction = Transaction(
            budget_id=budget.id,
            member_id=message.from_user.id,
            date=datetime.now(),
            outcome=10,
        )

        MongoTransactions().add(transaction)
        budgets.update_balance(transaction)

    await message.answer(text='done')


@dp.message_handler(text=texts.VIEW_TRANSACTIONS, state='*')
async def get_transactions_function(message: Message):
    transactions = [
        transaction
        for budget in MongoBudgets().get_by_groups([
            group.id for group in MongoGroups().get_by_member(message.from_user.id)
        ])
        for transaction in MongoTransactions().get_by_budget(budget.id)
    ]

    if not transactions:
        await message.answer(texts.NO_TRANSACTIONS)
        return

    for transaction in transactions:
        await message.answer(
            text=transaction.message_view,
            reply_markup=transaction_keyboard(transaction.id),
        )


@dp.callback_query_handler(Text(startswith=callbacks.REMOVE_TRANSACTION[:2]), state='*')
async def remove_transaction(callback: CallbackQuery):
    try:
        action, transaction_id = callback.data.split('-')
    except ValueError:
        # TODO: log failure
        return

    transaction = MongoTransactions().remove(transaction_id)
    MongoBudgets().update_balance(transaction, on_removing=True)

    await bot.delete_message(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
    )

    await callback.answer(texts.TRANSACTION_REMOVED, show_alert=True)


@dp.callback_query_handler(Text(startswith=callbacks.VIEW_TRANSACTIONS_OF_BUDGET[:2]), state='*')
async def show_transactions_of_budget(callback: CallbackQuery):
    try:
        action, budget_id = callback.data.split('-')
    except ValueError:
        # TODO: log failure
        return

    await bot.send_message(
        chat_id=callback.from_user.id,
        text=texts.YOUR_TRANSACTIONS_OF_BUDGET,
    )

    for transaction in MongoTransactions().get_by_budget(budget_id):
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=transaction.message_view,
            reply_markup=transaction_keyboard(transaction.id),
        )

    await callback.answer('👍')  # TODO
