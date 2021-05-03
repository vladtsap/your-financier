import logging

from aiogram.utils import executor

import middlewares
from config import bot
from handlers import dp
from models.commands import commands


# noinspection PyUnusedLocal
async def on_startup(dp):
    middlewares.setup(dp)
    await bot.set_my_commands(commands)
    logging.warning('bot started')


if __name__ == '__main__':
    executor.start_polling(
        dp,
        on_startup=on_startup
    )
