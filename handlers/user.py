from aiogram.types import Message

from config import dp
from keyboards.reply import start_keyboard
from models.core import Group, Member
from models.states import MainStates
from utils import texts
from utils.mongo import MongoGroup, MongoMember


@dp.message_handler(commands=['start'], state='*')
async def start_function(message: Message):
    member = Member(
        id=message.from_user.id,
        name=message.from_user.full_name,
    )

    if MongoMember().is_new(member):
        MongoGroup().add(
            Group(
                name='personal',
                members=[member.id],
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
        group = MongoGroup().get_by_id(invite_id)  # TODO: get ready for exception here
        MongoGroup().add_member(group, member.id)

    MongoMember().add(member)

    await MainStates.general.set()
