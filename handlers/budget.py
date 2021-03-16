from datetime import datetime

from aiogram.types import Message

from config import dp
from models.core import Budget, BudgetType, BudgetAdding, MainStates
from utils.mongo.budgets import add_budget, get_budget_by_groups
from utils.mongo.groups import get_groups_by_member

budget_in_process = {}  # id-to-budget  # TODO: move to redis


@dp.message_handler(commands=['add_budget'], state='*')
async def add_budget_function(message: Message):
    await BudgetAdding.name.set()
    await message.answer('send budget name')


@dp.message_handler(state=BudgetAdding.name)
async def add_budget_name(message: Message):
    budget_in_process[message.from_user.id] = {
        'name': message.text
    }
    await BudgetAdding.type.set()
    await message.answer('send budget type')


@dp.message_handler(state=BudgetAdding.type)
async def add_budget_type(message: Message):
    budget_in_process[message.from_user.id]['type'] = BudgetType(message.text)
    await BudgetAdding.amount.set()
    await message.answer('send budget amount')


@dp.message_handler(state=BudgetAdding.amount)
async def add_budget_amount(message: Message):
    budget_in_process[message.from_user.id]['amount'] = float(message.text)
    await BudgetAdding.rollover.set()
    await message.answer('should it be rollover?')


@dp.message_handler(state=BudgetAdding.rollover)
async def add_budget_rollover(message: Message):
    group = get_groups_by_member(message.from_user.id)[0]
    budget_content = budget_in_process[message.from_user.id]

    budget = Budget(
        name=budget_content['name'],
        type=budget_content['type'],
        start=datetime.now(),
        amount=budget_content['amount'],
        left=budget_content['amount'],
        rollover=bool(message.text),  # TODO: fix this
        group_id=group.id,
    )

    add_budget(budget)

    await MainStates.general.set()

    await message.answer('done')


@dp.message_handler(commands=['get_budget'], state='*')
async def get_budgets_function(message: Message):
    for budget in get_budget_by_groups([
        group.id for group in get_groups_by_member(message.from_user.id)
    ]):
        await message.answer(str(budget.to_dict()))
