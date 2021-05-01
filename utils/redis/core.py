import redis

from config import REDIS_HOST, REDIS_PORT
from models.core import Singleton


class RedisBase(metaclass=Singleton):

    def __init__(self, db: int):
        self.db = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=db,
        )

    @staticmethod
    def _decode_dict(d: dict):
        return {k.decode('utf-8'): v.decode('utf-8') for k, v in d.items()}
