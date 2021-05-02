from dataclasses import replace
from datetime import datetime

from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from pytz import timezone

from config import dp, bot
from keyboards.inline import transaction_keyboard
from keyboards.reply import start_keyboard, available_budgets_keyboard, transaction_types_keyboard
from models import callbacks
from models.core import Transaction
from models.states import TransactionAdding, MainStates
from utils import texts
from utils.mongo import (
    MongoGroup,
    MongoBudget,
    MongoTransaction,
)
from utils.redis import RedisTransaction


@dp.message_handler(text=texts.ADD_TRANSACTION, state='*')
async def add_transaction_function(message: Message):
    budgets = [budget.name for budget in MongoBudget().get_by_groups([
        group.id for group in MongoGroup().get_by_member(message.from_user.id)
    ])]

    if not budgets:
        await message.answer(texts.NO_BUDGETS)
        await MainStates.general.set()
        return

    await TransactionAdding.budget.set()
    await message.answer(
        text=texts.SELECT_TRANSACTION_BUDGET,
        reply_markup=available_budgets_keyboard(budgets),
    )


@dp.message_handler(state=TransactionAdding.budget)
async def add_budget_type(message: Message):
    RedisTransaction().add(
        user_id=message.from_user.id,
        key='budget_id',
        value=MongoBudget().get_by_name(message.text).id,
    )

    await TransactionAdding.type.set()
    await message.answer(
        text=texts.ENTER_TRANSACTION_TYPE,
        reply_markup=transaction_types_keyboard,
    )


@dp.message_handler(state=TransactionAdding.type)
async def add_budget_type(message: Message):
    RedisTransaction().add(
        user_id=message.from_user.id,
        key='spend',
        value=str(message.text == texts.TRANSACTION_SPEND),
    )

    await TransactionAdding.amount.set()
    await message.answer(texts.ENTER_TRANSACTION_AMOUNT)


@dp.message_handler(state=TransactionAdding.amount)
async def adding_transaction(message: Message):
    transaction_content = RedisTransaction().pop(message.from_user.id)

    transaction = Transaction(
        budget_id=transaction_content['budget_id'],
        member_id=message.from_user.id,
        date=datetime.now(timezone('Europe/Kiev')),
    )

    if transaction_content['spend'] == 'True':
        transaction = replace(transaction, outcome=float(message.text))
    else:
        transaction = replace(transaction, income=float(message.text))

    MongoTransaction().add(transaction)
    MongoBudget().update_balance(transaction)

    await MainStates.general.set()
    await message.answer(
        text=texts.TRANSACTION_ADDED,
        reply_markup=start_keyboard,
    )


@dp.message_handler(text=texts.VIEW_TRANSACTIONS, state='*')
async def get_transactions_function(message: Message):
    transactions = [
        transaction
        for budget in MongoBudget().get_by_groups([
            group.id for group in MongoGroup().get_by_member(message.from_user.id)
        ])
        for transaction in MongoTransaction().get_by_budget(budget.id)
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

    transaction = MongoTransaction().remove(transaction_id)
    MongoBudget().update_balance(transaction, on_removing=True)

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

    for transaction in MongoTransaction().get_by_budget(budget_id):
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=transaction.message_view,
            reply_markup=transaction_keyboard(transaction.id),
        )

    await callback.answer('👍')  # TODO


@dp.callback_query_handler(Text(startswith=callbacks.ADD_TRANSACTION_TO_BUDGET[:2]), state='*')
async def add_transaction_to_budget(callback: CallbackQuery):
    try:
        action, budget_id = callback.data.split('-')
    except ValueError:
        # TODO: log failure
        return
    else:
        await callback.answer('👍')  # TODO

    RedisTransaction().add(
        user_id=callback.from_user.id,
        key='budget_id',
        value=budget_id,
    )

    await TransactionAdding.type.set()
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=texts.ENTER_TRANSACTION_TYPE,
        reply_markup=transaction_types_keyboard,
    )
