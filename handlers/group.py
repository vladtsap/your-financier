from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram.utils.deep_linking import get_start_link

from config import dp, bot
from keyboards.inline import group_keyboard
from keyboards.reply import remove_keyboard, start_keyboard
from models import callbacks
from models.core import Group
from models.states import MainStates, GroupCreating
from utils import texts
from utils.mongo import MongoGroup


@dp.message_handler(commands=['new_group'], state='*')
async def create_new_group(message: Message):
    await GroupCreating.name.set()
    await message.answer(
        texts.ENTER_GROUP_NAME,
        reply_markup=remove_keyboard,
    )


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
        await get_start_link(group_id),
        reply_markup=start_keyboard,
    )


@dp.message_handler(commands=['view_groups'], state='*')
async def view_groups(message: Message):
    for group in MongoGroup().get_by_member(message.from_user.id):
        if group.name == 'personal':
            await message.answer(group.message_view)
        else:
            await message.answer(
                group.message_view,
                reply_markup=group_keyboard(group.id)
            )


@dp.callback_query_handler(Text(startswith=callbacks.REMOVE_GROUP[:2]), state='*')
async def remove_group(callback: CallbackQuery):
    try:
        action, group_id = callback.data.split('-')
    except ValueError:
        # TODO: log failure
        return

    MongoGroup().remove(group_id)

    await bot.delete_message(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
    )

    await callback.answer(texts.GROUP_REMOVED, show_alert=True)


@dp.callback_query_handler(Text(startswith=callbacks.GROUP_INVITE_LINK[:2]), state='*')
async def invite_to_group(callback: CallbackQuery):
    try:
        action, group_id = callback.data.split('-')
    except ValueError:
        # TODO: log failure
        return
    else:
        await callback.answer('👍')

    await bot.send_message(
        chat_id=callback.from_user.id,
        text=await get_start_link(group_id),
        reply_markup=start_keyboard,
    )
