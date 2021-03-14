from aiogram.types import Message

from config import dp
from models.core import Group
from utils.mongo.groups import (
    is_registered,
    add_solo_group,
)


@dp.message_handler(state='*', commands=['start'])
async def hello_function(message: Message):
    member_id = message.from_user.id
    if is_registered(message.from_user.id):
        await message.answer(text='glad to see you here again')

    else:
        add_solo_group(Group(
            name='personal',
            members=[member_id],
        ))
        await message.answer(text='hello there')
