from aiogram.types import Message

from config import dp
from keyboards.reply import start_keyboard
from models.core import Group
from models.states import MainStates
from utils import texts
from utils.mongo import MongoGroup


@dp.message_handler(commands=['start'], state='*')
async def start_function(message: Message):
    member_id = message.from_user.id
    if MongoGroup().is_new(message.from_user.id):
        MongoGroup().add(
            Group(
                name='personal',
                members=[member_id],
            )
        )
        await message.answer(
            text=texts.WELCOME,
            reply_markup=start_keyboard,
        )

    else:
        await message.answer(
            text=texts.MAIN_MENU,
            reply_markup=start_keyboard,
        )

    if invite_id := message.get_args():
        group = MongoGroup().get_by_id(invite_id)
        MongoGroup().add_member(group, member_id)

    await MainStates.general.set()
