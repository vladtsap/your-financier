from aiogram.dispatcher.filters.state import StatesGroup, State


class MainStates(StatesGroup):
    general = State()


class BudgetAdding(StatesGroup):
    group = State()
    name = State()
    type = State()
    amount = State()
    rollover = State()


class TransactionAdding(StatesGroup):
    budget = State()
    type = State()
    category = State()
    amount = State()


class BankConnection(StatesGroup):
    budget = State()
    token = State()


class GroupCreating(StatesGroup):
    name = State()
