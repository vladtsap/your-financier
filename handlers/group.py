from aiogram.types import Message
from aiogram.utils.deep_linking import get_start_link

from config import dp
from models.core import Group
from models.states import MainStates, GroupCreating
from utils import texts
from utils.mongo import MongoGroup


@dp.message_handler(commands=['new_group'], state='*')
async def create_new_group(message: Message):
    await GroupCreating.name.set()
    await message.answer(texts.ENTER_GROUP_NAME)


@dp.message_handler(state=GroupCreating.name)
async def creating_group(message: Message):
    group_id = MongoGroup().add(
        Group(
            name=message.text,
            members=[message.from_user.id],
        )
    )

    await MainStates.general.set()
    await message.answer(
        await get_start_link(group_id)
    )
