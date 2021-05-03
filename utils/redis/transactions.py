from config import REDIS_DB_TP
from utils.redis.core import RedisBase


class RedisTransaction(RedisBase):

    def __init__(self):
        super(RedisTransaction, self).__init__(REDIS_DB_TP)
