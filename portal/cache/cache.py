import time
from portal.func.functionCommon import convert_to_dict
from portal.Constant import *
import redis
import json

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


class BaseCache:
    current_size = 0
    exchange_size = 0
    heap_name = ''
    vsset_name = ''
    hmset_name = ''

    def __init__(self):
        return

    def add_cache(self, key, value):
        if self.current_size > self.exchange_size:
            self.shrink()
        self.current_size += 1
        now = float(time.time())
        r.hset(self.hmset_name, key, value)
        r.zadd(self.heap_name, key, -now)
        r.hset(self.vsset_name, key, str(now))
        return

    def shrink(self):
        del_keys = r.zrevrangebyscore(self.heap_name, 0, self.current_size - self.exchange_size)
        for i in del_keys:
            r.zrem(self.heap_name, i[0])
            r.hdel(self.vsset_name, i[0])
            r.hdel(self.hmset_name, i[0])
            self.current_size -= 1
        return

    def init(self, name, exchange_size):
        self.hmset_name = "cache:" + name
        self.heap_name = "heap:" + name
        self.vsset_name = "vsset:" + name
        self.current_size = r.hlen(self.hmset_name)
        self.exchange_size = exchange_size

    def get_cache_obj(self, key):
        return

    def get_cache(self, key, timestamp):
        result = r.hget(self.hmset_name, key)
        print result
        if not result or len(result) == 0:
            obj = self.get_cache_obj(key)
            obj_json = json.dumps(obj)
            self.add_cache(key, obj_json)
            return obj_json
        version = r.hget(self.vsset_name, key)
        if version:
            r.zrem(self.heap_name, key)
        else:
            version = '0'
        if not version:
            version = 0
        if float(version) < timestamp:
            return result
        else:
            return NO_THIS_CACHE
