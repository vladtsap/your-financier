from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from middlewares.throttling import ThrottlingMiddleware
from middlewares.admin_only import AccessMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(AccessMiddleware(148111610))  # TODO: remove before release
