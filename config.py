import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from envparse import env

TELEGRAM_TOKEN = env.str("TELEGRAM_TOKEN", default='1594794180:AAF9xVlstCdoSzwQKyAxacscXtGS6bz50PU')

REDIS_HOST = env.str("REDIS_HOST", default='localhost')
REDIS_PORT = env.int("REDIS_PORT", default=6379)
REDIS_DB_FSM = env.int("REDIS_DB_FSM", default=0)
REDIS_DB_BP = env.int("REDIS_DB_BP", default=1)

MONGO_HOST = env.str("MONGO_HOST", default="localhost")
MONGO_USER = env.str("MONGO_USER", default="root")
MONGO_PASSWORD = env.str("MONGO_PASSWORD", default="password")
MONGO_PORT = env.int("MONGO_PORT", default=27017)
MONGO_URL = f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/'

THROTTLING_LIMIT = env.float("THROTTLING_LIMIT", default=0.1)

ADMIN_ID = [148111610]

storage = RedisStorage2(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_FSM)
bot = Bot(token=TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML, validate_token=True)
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(
    format=u'[%(asctime)s] %(levelname)-8s %(message)s',
    level=logging.INFO,
    # filename="bot.log",
)
