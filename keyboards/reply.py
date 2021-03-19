from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)

from utils import texts

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(texts.ADD_BUDGET), KeyboardButton(texts.ADD_TRANSACTION)],
        [KeyboardButton(texts.VIEW_BUDGETS), KeyboardButton(texts.VIEW_TRANSACTION)],
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

budget_rollover = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(texts.DO_ROLLOVER), KeyboardButton(texts.DO_NOT_ROLLOVER)],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
