from config import REDIS_DB_BP
from utils.redis.core import RedisBase


class RedisBudget(RedisBase):

    def __init__(self):
        super(RedisBudget, self).__init__(REDIS_DB_BP)

    def add(self, user_id: int, key: str, value: str):
        self.db.hset(user_id, key, value)

    def get(self, user_id: int, key: str) -> str:
        return self.db.hget(user_id, key).decode('utf-8')

    def pop(self, user_id: int) -> dict:
        data = self._decode_dict(self.db.hgetall(user_id))
        self.db.hdel(user_id, *data.keys())
        return data
