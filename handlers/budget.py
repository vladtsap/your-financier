from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from config import dp, bot
from keyboards.inline import budget_keyboard
from keyboards.reply import (
    start_keyboard,
    remove_keyboard,
    budget_types_keyboard,
    budget_rollover_keyboard,
    options_keyboard,
)
from models import callbacks
from models.core import Budget, BudgetType
from models.states import MainStates, BudgetAdding
from utils import texts
from utils.mongo import MongoGroup, MongoBudget
from utils.redis import RedisBudget


@dp.message_handler(text=texts.ADD_BUDGET, state='*')
async def add_budget_function(message: Message):
    groups = [
        group.name for group in MongoGroup().get_by_member(message.from_user.id)
    ]

    await BudgetAdding.group.set()
    await message.answer(
        text=texts.ENTER_BUDGET_GROUP,
        reply_markup=options_keyboard(groups),
    )


@dp.message_handler(state=BudgetAdding.group)
async def add_budget_group(message: Message):
    RedisBudget().add(
        user_id=message.from_user.id,
        key='group_id',
        value=MongoGroup().get_by_name(message.text).id,
    )
    await BudgetAdding.name.set()
    await message.answer(
        text=texts.ENTER_BUDGET_NAME,
        reply_markup=remove_keyboard,
    )


@dp.message_handler(state=BudgetAdding.name)
async def add_budget_name(message: Message):
    RedisBudget().add(
        user_id=message.from_user.id,
        key='name',
        value=message.text,
    )
    await BudgetAdding.type.set()
    await message.answer(
        text=texts.ENTER_BUDGET_TYPE,
        reply_markup=budget_types_keyboard,
    )


@dp.message_handler(state=BudgetAdding.type)
async def add_budget_type(message: Message):
    RedisBudget().add(
        user_id=message.from_user.id,
        key='type',
        value=BudgetType(message.text).value,
    )
    await BudgetAdding.amount.set()
    await message.answer(texts.ENTER_BUDGET_AMOUNT)


@dp.message_handler(state=BudgetAdding.amount)
async def add_budget_amount(message: Message):
    rb = RedisBudget()
    rb.add(
        user_id=message.from_user.id,
        key='amount',
        value=message.text,
    )
    if rb.get(user_id=message.from_user.id, key='type') == BudgetType.ONE_TIME.value:
        await adding_budget(message)
    else:
        await BudgetAdding.rollover.set()
        await message.answer(
            text=texts.ENTER_BUDGET_ROLLOVER,
            reply_markup=budget_rollover_keyboard,
        )


@dp.message_handler(state=BudgetAdding.rollover)
async def add_budget_rollover(message: Message):
    RedisBudget().add(
        user_id=message.from_user.id,
        key='rollover',
        value=str(message.text == texts.DO_ROLLOVER),
    )
    await adding_budget(message)


async def adding_budget(message: Message):
    budget_content = RedisBudget().pop(message.from_user.id)

    budget = Budget(
        name=budget_content['name'],
        type=BudgetType(budget_content['type']),
        amount=float(budget_content['amount']),
        left=float(budget_content['amount']),
        rollover=budget_content.get('rollover', 'False') == 'True',
        group_id=MongoGroup().get_by_id(budget_content['group_id']).id,
    )

    MongoBudget().add(budget)

    await MainStates.general.set()
    await message.answer(
        text=texts.BUDGET_ADDED,
        reply_markup=start_keyboard,
    )


@dp.message_handler(text=texts.VIEW_BUDGETS, state='*')
async def get_budgets_function(message: Message):
    budgets = MongoBudget().get_by_groups([
        group.id for group in MongoGroup().get_by_member(message.from_user.id)
    ])

    if not budgets:
        await message.answer(texts.NO_BUDGETS)
        return

    for budget in budgets:
        await message.answer(
            text=budget.message_view,
            reply_markup=budget_keyboard(budget.id),
        )


@dp.callback_query_handler(Text(startswith=callbacks.REMOVE_BUDGET[:2]), state='*')
async def remove_budget(callback: CallbackQuery):
    try:
        action, budget_id = callback.data.split('-')
    except ValueError:
        # TODO: log failure
        return

    MongoBudget().remove(budget_id)

    await bot.delete_message(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
    )

    await callback.answer(texts.BUDGET_REMOVED, show_alert=True)
