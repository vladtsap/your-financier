from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)

from models.core import Categories
from utils import texts

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(texts.ADD_BUDGET), KeyboardButton(texts.ADD_TRANSACTION)],
        [KeyboardButton(texts.VIEW_BUDGETS), KeyboardButton(texts.VIEW_TRANSACTIONS)],
    ],
    resize_keyboard=True,
)

remove_keyboard = ReplyKeyboardRemove()

budget_types_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(texts.WEEKLY), KeyboardButton(texts.MONTHLY)],
        [KeyboardButton(texts.YEARLY), KeyboardButton(texts.ONE_TIME)],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

budget_rollover_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(texts.DO_ROLLOVER), KeyboardButton(texts.DO_NOT_ROLLOVER)],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


def available_budgets_keyboard(budgets: list) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [budget] for budget in budgets
        ],
        resize_keyboard=True,
    )


transaction_types_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(texts.TRANSACTION_RECEIVE),
            KeyboardButton(texts.TRANSACTION_SPEND)
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


def transaction_categories_keyboard(spend: bool) -> ReplyKeyboardMarkup:
    categories = Categories.suggested_spending() if spend else Categories.suggested_earning()
    return ReplyKeyboardMarkup(
        keyboard=[
            [category] for category in categories
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
