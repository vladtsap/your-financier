from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class BudgetType(Enum):
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'


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
    start: datetime
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


@dataclass
class Transaction:
    budget_id: str
    member_id: int
    date: datetime
    outcome: float = field(default=0.)
    income: float = field(default=0.)
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
