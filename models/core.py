from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional

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
    start: datetime  # TODO: think about this
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
            start=datetime.fromisoformat(data['start']),
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
            'start': self.start.isoformat(),
            'amount': self.amount,
            'left': self.left,
            'rollover': self.rollover,
            'group_id': self.group_id,
        }

        if self.id:
            result['_id'] = self.id

        return result

    @property
    def message_view(self) -> str:
        result = f'<b>{texts.MSG_BUDGET_NAME}:</b> {self.name}\n' \
                 f'<b>{texts.MSG_BUDGET_TYPE}:</b> {self.type.value}\n' \
                 f'<b>{texts.MSG_BUDGET_AMOUNT}:</b> {self.amount}\n' \
                 f'<b>{texts.MSG_BUDGET_LEFT}:</b> {self.left}\n' \
                 f'<b>{texts.MSG_BUDGET_ROLLOUT}:</b> {self.rollover}'

        # TODO: fix type
        # TODO: add group

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
        from utils.mongo import MongoBudgets
        result = f'<b>{texts.MSG_TRANSACTION_DATE}:</b> ' \
                 f'{self.date.day:02}.{self.date.month:02} ' \
                 f'{self.date.hour:02}:{self.date.minute:02}\n'

        if self.outcome:
            result += f'<b>{texts.MSG_TRANSACTION_OUTCOME}:</b> {self.outcome:.2f}₴\n'

        if self.income:
            result += f'<b>{texts.MSG_TRANSACTION_INCOME}:</b> {self.income:.2f}₴\n'

        if self.note:
            result += f'<b>{texts.MSG_TRANSACTION_NOTE}:</b> {self.note}\n'

        budget = MongoBudgets().get_by_id(self.budget_id)
        result += f'<b>{texts.MSG_TRANSACTION_BUDGET_NAME}:</b> {budget.name}\n'

        # TODO: add spender name

        return result


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
