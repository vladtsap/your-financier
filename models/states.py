from aiogram.dispatcher.filters.state import StatesGroup, State


class MainStates(StatesGroup):
    general = State()


class BudgetAdding(StatesGroup):
    name = State()
    type = State()
    amount = State()
    rollover = State()


class TransactionAdding(StatesGroup):
    budget = State()
    type = State()
    amount = State()
