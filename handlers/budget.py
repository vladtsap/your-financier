from datetime import datetime

from aiogram.types import Message

from config import dp
from keyboards.reply import (
    start_keyboard,
    remove_keyboard,
    budget_types_keyboard,
    budget_rollover,
)
from models.core import Budget, BudgetType
from models.states import MainStates, BudgetAdding
from utils import texts
from utils.mongo.budgets import MongoBudgets
from utils.mongo.groups import MongoGroups

budget_in_process = {}  # id-to-budget  # TODO: move to redis

text_to_budget_type = {
    texts.WEEKLY: BudgetType.WEEKLY,
    texts.MONTHLY: BudgetType.MONTHLY,
    texts.YEARLY: BudgetType.YEARLY,
    texts.ONE_TIME: BudgetType.ONE_TIME,
}


@dp.message_handler(text=texts.ADD_BUDGET, state='*')
async def add_budget_function(message: Message):
    await BudgetAdding.name.set()
    await message.answer(
        text=texts.ENTER_BUDGET_NAME,
        reply_markup=remove_keyboard,
    )


@dp.message_handler(state=BudgetAdding.name)
async def add_budget_name(message: Message):
    budget_in_process[message.from_user.id] = {
        'name': message.text
    }
    await BudgetAdding.type.set()
    await message.answer(
        text=texts.ENTER_BUDGET_TYPE,
        reply_markup=budget_types_keyboard,
    )


@dp.message_handler(state=BudgetAdding.type)
async def add_budget_type(message: Message):
    budget_in_process[message.from_user.id]['type'] = text_to_budget_type[message.text]
    await BudgetAdding.amount.set()
    await message.answer(texts.ENTER_BUDGET_AMOUNT)


@dp.message_handler(state=BudgetAdding.amount)
async def add_budget_amount(message: Message):
    budget_in_process[message.from_user.id]['amount'] = float(message.text)

    if budget_in_process[message.from_user.id]['type'] == BudgetType.ONE_TIME:
        await adding_budget(message)
    else:
        await BudgetAdding.rollover.set()
        await message.answer(
            text=texts.ENTER_BUDGET_ROLLOVER,
            reply_markup=budget_rollover,
        )


@dp.message_handler(state=BudgetAdding.rollover)
async def add_budget_rollover(message: Message):
    budget_in_process[message.from_user.id]['rollover'] = message.text == texts.DO_ROLLOVER
    await adding_budget(message)


async def adding_budget(message: Message):
    group = MongoGroups().get_by_member(message.from_user.id)[0]  # TODO: workaround
    budget_content = budget_in_process.pop(message.from_user.id)

    budget = Budget(
        name=budget_content['name'],
        type=budget_content['type'],
        start=datetime.now(),
        amount=budget_content['amount'],
        left=budget_content['amount'],
        rollover=budget_content.get('rollover') or False,
        group_id=group.id,
    )

    MongoBudgets().add(budget)

    await MainStates.general.set()
    await message.answer(
        text=texts.BUDGET_ADDED,
        reply_markup=start_keyboard,
    )


@dp.message_handler(text=texts.VIEW_BUDGETS, state='*')
async def get_budgets_function(message: Message):
    for budget in MongoBudgets().get_by_groups([
        group.id for group in MongoGroups().get_by_member(message.from_user.id)
    ]):
        await message.answer(budget.message_view)
