from typing import List

from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message


class AccessMiddleware(BaseMiddleware):
    def __init__(self, access_ids: List[int]):
        self.access_ids = access_ids
        super().__init__()

    async def on_process_message(self, message: Message, _):
        if message.from_user.id not in self.access_ids:
            raise CancelHandler()
