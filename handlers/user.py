from aiogram.types import Message

from config import dp


@dp.message_handler(state='*', commands=['start'])
async def hello_function(message: Message):
    await message.answer(text='hello')
