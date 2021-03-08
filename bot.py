import logging

from aiogram.utils import executor

import middlewares
from handlers import dp


# noinspection PyUnusedLocal
async def on_startup(dp):
    middlewares.setup(dp)
    logging.warning('bot started')


if __name__ == '__main__':
    executor.start_polling(
        dp,
        on_startup=on_startup
    )
