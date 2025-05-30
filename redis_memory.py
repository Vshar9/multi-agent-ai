import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

class RedisMemory:
    def __init__(self):
        self.client = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT")),
            db=int(os.getenv("REDIS_DB", 0)),
            decode_responses=True,
            username=os.getenv("REDIS_USERNAME"),
            password=os.getenv("REDIS_PASSWORD")
        )

    def set_value(self, key: str, value: dict):
        self.client.set(key, json.dumps(value))

    def get_value(self, key: str):
        val = self.client.get(key)
        if val:
            return json.loads(val)
        return None

    def push_to_list(self, list_name: str, value: dict):
        self.client.rpush(list_name, json.dumps(value))

    def get_list(self, list_name: str):
        items = self.client.lrange(list_name, 0, -1)
        return [json.loads(item) for item in items]

    def clear_memory(self):
        self.client.flushdb()


if __name__ == "__main__":
    mem = RedisMemory()
    mem.set_value("test", {"env_check": True})
    print(mem.get_value("test"))

