from config import REDIS_DB_BP
from utils.redis.core import RedisBase


class RedisBudget(RedisBase):

    def __init__(self):
        super(RedisBudget, self).__init__(REDIS_DB_BP)
