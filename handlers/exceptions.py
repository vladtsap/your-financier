import logging

from aiogram.utils.exceptions import (
    CantDemoteChatCreator,
    MessageNotModified,
    MessageCantBeDeleted,
    MessageToDeleteNotFound,
    MessageTextIsEmpty,
    Unauthorized,
    InvalidQueryID,
    TelegramAPIError,
    RetryAfter,
    CantParseEntities,
)

from config import dp


@dp.errors_handler()
async def default_errors_handler(update, exception):
    if isinstance(exception, CantDemoteChatCreator):
        logging.debug("Can't demote chat creator")
        return True

    if isinstance(exception, MessageNotModified):
        logging.error('Message is not modified')
        return True

    if isinstance(exception, MessageCantBeDeleted):
        logging.debug('Message cant be deleted')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logging.error('Message to delete not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logging.error('MessageTextIsEmpty')
        return True

    if isinstance(exception, Unauthorized):
        logging.info(f'Unauthorized: {exception}')
        return True

    if isinstance(exception, InvalidQueryID):
        logging.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, TelegramAPIError):
        logging.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, RetryAfter):
        logging.exception(f'RetryAfter: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, CantParseEntities):
        logging.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True

