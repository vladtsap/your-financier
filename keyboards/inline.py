from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from models import callbacks
from utils import texts


def budget_keyboard(budget_id: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=texts.REMOVE_BUDGET,
                    callback_data=callbacks.REMOVE_BUDGET.format(budget_id=budget_id),
                )
            ],
            [
                InlineKeyboardButton(
                    text=texts.VIEW_TRANSACTIONS_OF_BUDGET,
                    callback_data=callbacks.VIEW_TRANSACTIONS_OF_BUDGET.format(budget_id=budget_id),
                )
            ],
        ]
    )


def transaction_keyboard(transaction_id: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=texts.REMOVE_TRANSACTION,
                    callback_data=callbacks.REMOVE_TRANSACTION.format(transaction_id=transaction_id),
                )
            ],
            [
                InlineKeyboardButton(
                    text=texts.TRANSFER_INTO_ANOTHER_BUDGET,
                    callback_data=callbacks.TRANSFER_INTO_ANOTHER_BUDGET.format(transaction_id=transaction_id),
                )
            ],
        ]
    )
