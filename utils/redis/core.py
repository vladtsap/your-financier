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

    def add(self, user_id: int, key: str, value: str):
        self.db.hset(user_id, key, value)

    def get(self, user_id: int, key: str) -> str:
        return self.db.hget(user_id, key).decode('utf-8')

    def pop(self, user_id: int) -> dict:
        data = self._decode_dict(self.db.hgetall(user_id))
        self.db.hdel(user_id, *data.keys())
        return data

    @staticmethod
    def _decode_dict(d: dict):
        return {k.decode('utf-8'): v.decode('utf-8') for k, v in d.items()}
