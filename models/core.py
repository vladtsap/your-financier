from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional

from pytz import timezone

from utils import texts


class ExtendedEnum(Enum):
    @property
    def value(self):
        return super().value[0]

    @property
    def verbose_name(self):
        return super().value[1]

    @classmethod
    def _missing_(cls, key):
        for item in cls:
            if item.value == key or item.verbose_name == key:
                return item
        return super()._missing_(key)


class BudgetType(ExtendedEnum):
    WEEKLY = ('weekly', texts.WEEKLY)
    MONTHLY = ('monthly', texts.MONTHLY)
    YEARLY = ('yearly', texts.MONTHLY)
    ONE_TIME = ('one-time', texts.ONE_TIME)


class Categories(ExtendedEnum):
    AUTO = ('auto', texts.AUTO_CATEGORY)
    BOOKS = ('books', texts.BOOKS_CATEGORY)
    CLOTHES = ('clothes', texts.CLOTHES_CATEGORY)
    ENTERTAINMENT = ('entertainment', texts.ENTERTAINMENT_CATEGORY)
    FEES = ('fees', texts.FEES_CATEGORY)
    FOOD = ('food', texts.FOOD_CATEGORY)
    GIFTS = ('gifts', texts.GIFTS_CATEGORY)
    HEALTH = ('health', texts.HEALTH_CATEGORY)
    HOME = ('home', texts.HOME_CATEGORY)
    PAYMENT = ('payment', texts.PAYMENT_CATEGORY)
    SALARY = ('salary', texts.SALARY_CATEGORY)
    SUPERMARKET = ('supermarket', texts.SUPERMARKET_CATEGORY)
    TRANSPORT = ('transport', texts.TRANSPORT_CATEGORY)
    TRAVEL = ('travel', texts.TRAVEL_CATEGORY)
    OTHER = ('other', texts.OTHER_CATEGORY)

    @classmethod
    def spending(cls) -> tuple:
        return (
            cls.AUTO, cls.BOOKS, cls.CLOTHES, cls.ENTERTAINMENT, cls.FEES, cls.FOOD, cls.GIFTS,
            cls.HEALTH, cls.HOME, cls.PAYMENT, cls.SUPERMARKET, cls.TRANSPORT, cls.TRAVEL, cls.OTHER,
        )

    @classmethod
    def earning(cls) -> tuple:
        return (
            cls.GIFTS, cls.PAYMENT, cls.SALARY, cls.OTHER,
        )

    @classmethod
    def suggested_spending(cls) -> list:
        return [category.verbose_name for category in cls.spending()]

    @classmethod
    def suggested_earning(cls) -> list:
        return [category.verbose_name for category in cls.earning()]

    @classmethod
    def match(cls, mcc: int):

        if mcc in range(3351, 3442) or [
            5013, 5172, 5511, 5521, 5531, 5532, 5533, 5541, 5542, 5552, 5561, 5571, 5592, 5598, 5599,
            5935, 5983, 7511, 7512, 7513, 7519, 7523, 7524, 7531, 7534, 7535, 7538, 7542, 7549, 8675,
        ]:
            return cls.AUTO

        elif mcc in [5192, 5942, 5994]:
            return cls.BOOKS

        elif mcc in [
            5094, 5131, 5137, 5139, 5611, 5621, 5631, 5641, 5651, 5655, 5661, 5681, 5691, 5697, 5698,
            5699, 5931, 5948, 5949, 7251, 7296,
        ]:
            return cls.CLOTHES

        elif mcc in [
            5816, 7221, 7272, 7273, 7278, 7394, 7800, 7801, 7802, 7829, 7832, 7833, 7841, 7911, 7922,
            7929, 7932, 7933, 7941, 7993, 7994, 7995, 7996, 7997, 7998, 7999, 9406, 9754,
        ]:
            return cls.ENTERTAINMENT

        elif mcc in [
            6010, 6011, 6012, 6022, 6023, 6025, 6026, 6028, 6760, 7276, 7322, 9211, 9222, 9223, 9311,
            9399, 9405, 9411,
        ]:
            return cls.FEES

        elif mcc in [5811, 5812, 5813, 5814]:
            return cls.FOOD

        elif mcc in [5944, 5945, 5946, 5947, 5992]:
            return cls.GIFTS

        elif mcc in [
            4119, 5047, 5072, 5122, 5912, 5940, 5941, 5975, 5976, 5977, 5997, 7230, 7280, 7297, 7298,
            8011, 8021, 8031, 8041, 8042, 8043, 8044, 8049, 8062, 8071, 8099, 9702,
        ]:
            return cls.HEALTH

        elif mcc in [
            780, 1520, 1711, 1731, 1740, 1750, 1761, 1771, 2842, 4900, 5021, 5039, 5051, 5074, 5193,
            5198, 5200, 5211, 5231, 5251, 5261, 5271, 5299, 5712, 5713, 5714, 5718, 5719, 5722, 5732,
            5950, 6513, 7210, 7211, 7216, 7217, 7622, 7623, 7629, 7631, 7641, 7692, 7699, 8911,
        ]:
            return cls.HOME

        elif mcc in [
            3882, 4829, 6050, 6051, 6211, 6236, 6529, 6530, 6531, 6532, 6533, 6534, 6535, 6536, 6537,
            6538, 6539, 6540, 6611,
        ]:
            return cls.PAYMENT

        elif mcc in [
            743, 744, 5262, 5297, 5298, 5300, 5309, 5310, 5311, 5331, 5399, 5411, 5422, 5441, 5451,
            5462, 5499, 5715, 5921, 5993,
        ]:
            return cls.SUPERMARKET

        elif mcc in [4111, 4121, 4131, 4784, 5962]:
            return cls.TRANSPORT

        elif mcc in range(3000, 3303) or range(3501, 3839) or [
            4011, 4112, 4411, 4457, 4468, 4511, 4582, 4722, 4723, 4789, 5551, 7011, 7033, 7991, 7992,
        ]:
            return cls.TRAVEL

        else:
            return cls.OTHER


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

        today_transactions = MongoTransaction().get_all_for_today_by_budget(self.id)
        today_income = sum([transaction.income for transaction in today_transactions])
        today_outcome = sum([transaction.outcome for transaction in today_transactions])

        left_before_today = self.left + today_outcome - today_income
        amount_per_day = left_before_today / self.days_left

        return amount_per_day + today_income - today_outcome

    @property
    def message_view(self) -> str:

        result = f'💰 <b>{self.name}</b> — {self.amount:,.2f}₴\n' \
                 f'<b>{texts.MSG_BUDGET_TYPE}:</b> {self.type.verbose_name}\n' \
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
    category: Categories
    outcome: Optional[float] = field(default=0.)
    income: Optional[float] = field(default=0.)
    id: Optional[str] = field(default=None)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            budget_id=data['budget_id'],
            member_id=data['member_id'],
            date=datetime.fromisoformat(data['date']),
            outcome=data.get('outcome', 0.),
            income=data.get('income', 0.),
            category=Categories(data['category']),
            id=str(data.get('_id')),
        )

    def to_dict(self) -> dict:
        result = {
            'budget_id': self.budget_id,
            'member_id': self.member_id,
            'date': self.date.isoformat(),
            'outcome': self.outcome,
            'income': self.income,
            'category': self.category.value,
        }

        if self.id:
            result['_id'] = self.id

        return result

    @property
    def message_view(self) -> str:
        from utils.mongo import MongoBudget

        if self.outcome:
            result = f'📤 <b>-{self.outcome:,.2f}₴</b>\n'
        else:
            result = f'📥 <b>+{self.income:,.2f}₴</b>\n'

        result += f'🗓 {self.date.day:02}.{self.date.month:02} {self.date.hour:02}:{self.date.minute:02}\n'

        budget = MongoBudget().get_by_id(self.budget_id)
        result += f'💰 {budget.name}\n' \
                  f'🏷 {self.category.verbose_name}\n'

        return result


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
