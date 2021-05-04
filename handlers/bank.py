import requests
from aiogram.types import Message

from config import dp
from keyboards.reply import available_budgets_keyboard, start_keyboard
from models.states import MainStates, BankConnection
from utils import texts
from utils.mongo import MongoBudget, MongoGroup
from utils.redis import RedisBank


@dp.message_handler(commands=['connect_bank'], state='*')
async def connect_bank(message: Message):
    budgets = [budget.name for budget in MongoBudget().get_by_groups([
        group.id for group in MongoGroup().get_by_member(message.from_user.id)
    ])]

    if not budgets:
        await message.answer(texts.NO_BUDGETS)
        await MainStates.general.set()
        return

    await BankConnection.budget.set()
    await message.answer(
        text=texts.SELECT_BANK_BUDGET,
        reply_markup=available_budgets_keyboard(budgets),

    )


@dp.message_handler(state=BankConnection.budget)
async def select_bank_budget(message: Message):
    RedisBank().add(
        user_id=message.from_user.id,
        key='budget_id',
        value=MongoBudget().get_by_name(message.text).id,
    )

    await BankConnection.token.set()
    await message.answer(texts.ENTER_BANK_TOKEN)


@dp.message_handler(state=BankConnection.token)
async def connecting_bank(message: Message):
    connection_content = RedisBank().pop(message.from_user.id)

    # TODO: check token and predict wrong answer

    # requests.post(
    #     'https://api.monobank.ua/personal/webhook',
    #     headers={
    #         'X-Token': message.text,
    #     },
    #     json={
    #         'webHookUrl': f"my-site.com/{connection_content['budget_id']}/path-where-to-catch-requests",
    #     }
    # )

    await MainStates.general.set()
    await message.answer(
        text=texts.BANK_CONNECTED,
        reply_markup=start_keyboard,
    )
