from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional

from pytz import timezone

from utils import texts


class BudgetType(Enum):
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'
    ONE_TIME = 'one-time'


@dataclass
class Group:
    name: str
    members: List[int]
    id: Optional[str] = field(default=None)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data['name'],
            members=data['members'],
            id=str(data.get('_id')),
        )

    def to_dict(self) -> dict:
        result = {
            'name': self.name,
            'members': self.members,
        }

        if self.id:
            result['_id'] = self.id

        return result


@dataclass
class Budget:
    name: str
    type: BudgetType
    amount: float
    left: float
    rollover: bool
    group_id: str
    id: Optional[str] = field(default=None)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data['name'],
            type=BudgetType(data['type']),
            amount=data['amount'],
            left=data['left'],
            rollover=data['rollover'],
            group_id=data['group_id'],
            id=str(data.get('_id')),
        )

    def to_dict(self) -> dict:
        result = {
            'name': self.name,
            'type': self.type.value,
            'amount': self.amount,
            'left': self.left,
            'rollover': self.rollover,
            'group_id': self.group_id,
        }

        if self.id:
            result['_id'] = self.id

        return result

    @property
    def days_left(self) -> int:
        today = datetime.now(timezone('Europe/Kiev'))

        if self.type == BudgetType.WEEKLY:
            return 7 - today.weekday()

        elif self.type == BudgetType.MONTHLY:
            start_of_month = today.replace(day=1) - timedelta(days=1)
            end_of_month = today.replace(day=28) + timedelta(days=4)
            end_of_month = end_of_month - timedelta(days=end_of_month.day)
            return (end_of_month - start_of_month).days + 1

        elif self.type == BudgetType.YEARLY:
            new_year = today.replace(day=1, month=1, year=today.year + 1)
            return (new_year - today).days

        elif self.type == BudgetType.ONE_TIME:
            return 1  # TODO

    @property
    def left_for_today(self) -> float:
        from utils.mongo import MongoTransaction
        amount_per_day = self.left / self.days_left

        today_transactions = MongoTransaction().get_all_for_today_by_budget(self.id)
        today_income = sum([transaction.income for transaction in today_transactions])
        today_outcome = sum([transaction.outcome for transaction in today_transactions])

        return amount_per_day + today_income - today_outcome

    @property
    def message_view(self) -> str:

        result = f'💰 <b>{self.name}</b> — {self.amount:,.2f}₴\n' \
                 f'<b>{texts.MSG_BUDGET_TYPE}:</b> {self.type.value}\n' \
                 f'<b>{texts.MSG_BUDGET_LEFT_PERIOD}:</b> {self.left:,.2f}₴\n'

        if self.type != BudgetType.ONE_TIME:
            result += f'<b>{texts.MSG_BUDGET_LEFT_TODAY}:</b> {self.left_for_today:,.2f}₴\n'

        result += f'<b>{texts.MSG_BUDGET_ROLLOUT}:</b> {"✅" if self.rollover else "❎"}'

        return result


@dataclass
class Transaction:
    budget_id: str
    member_id: int
    date: datetime
    outcome: Optional[float] = field(default=0.)
    income: Optional[float] = field(default=0.)
    note: Optional[str] = field(default=None)
    id: Optional[str] = field(default=None)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            budget_id=data['budget_id'],
            member_id=data['member_id'],
            date=datetime.fromisoformat(data['date']),
            outcome=data.get('outcome', 0.),
            income=data.get('income', 0.),
            note=data.get('note'),
            id=str(data.get('_id')),
        )

    def to_dict(self) -> dict:
        result = {
            'budget_id': self.budget_id,
            'member_id': self.member_id,
            'date': self.date.isoformat(),
            'outcome': self.outcome,
            'income': self.income,
            'note': self.note,
        }

        if self.id:
            result['_id'] = self.id

        return result

    @property
    def message_view(self) -> str:
        from utils.mongo import MongoBudget
        result = f'<b>{texts.MSG_TRANSACTION_DATE}:</b> ' \
                 f'{self.date.day:02}.{self.date.month:02} ' \
                 f'{self.date.hour:02}:{self.date.minute:02}\n'

        if self.outcome:
            result += f'<b>{texts.MSG_TRANSACTION_OUTCOME}:</b> {self.outcome:,.2f}₴\n'

        if self.income:
            result += f'<b>{texts.MSG_TRANSACTION_INCOME}:</b> {self.income:,.2f}₴\n'

        if self.note:
            result += f'<b>{texts.MSG_TRANSACTION_NOTE}:</b> {self.note}\n'

        budget = MongoBudget().get_by_id(self.budget_id)
        result += f'<b>{texts.MSG_TRANSACTION_BUDGET_NAME}:</b> {budget.name}\n'

        return result


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
