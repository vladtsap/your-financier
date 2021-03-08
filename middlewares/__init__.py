from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from middlewares.throttling import ThrottlingMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())
