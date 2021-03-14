from datetime import datetime

from aiogram.types import Message

from config import dp
from models.core import Budget, BudgetType
from utils.mongo.budgets import add_budget, get_budget_by_groups
from utils.mongo.groups import get_groups_by_member


@dp.message_handler(state='*', commands=['add_budget'])
async def add_budget_function(message: Message):
    group = get_groups_by_member(message.from_user.id)[0]

    budget = Budget(
        name='test',
        type=BudgetType.WEEKLY,
        start=datetime.now(),
        amount=100,
        left=100,
        rollover=False,
        group_id=group.id,
    )
    add_budget(budget)

    await message.answer(text='done')


@dp.message_handler(state='*', commands=['get_budget'])
async def get_budgets_function(message: Message):
    for budget in get_budget_by_groups([
        group.id for group in get_groups_by_member(message.from_user.id)
    ]):
        await message.answer(str(budget.to_dict()))
