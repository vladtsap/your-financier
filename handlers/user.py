from aiogram.types import Message

from config import dp
from keyboards.reply import start_keyboard
from models.core import Group
from models.states import MainStates
from utils import texts
from utils.mongo import MongoGroups


@dp.message_handler(commands=['start'], state='*')
async def start_function(message: Message):
    member_id = message.from_user.id
    if MongoGroups().is_new(message.from_user.id):
        MongoGroups().add(
            Group(
                name='personal',
                members=[member_id],
            )
        )
        await message.answer(text=texts.WELCOME)

    else:
        await message.answer(
            text=texts.MAIN_MENU,
            reply_markup=start_keyboard,
        )

    await MainStates.general.set()
