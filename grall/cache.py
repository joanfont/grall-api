import collections
from functools import wraps
import json

import redis

from grall.config import config


connection = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)


def remember(key_prefix, ttl, encoder=None, decoder=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args):

            hashable_args = list(filter(lambda x: isinstance(x, str), args))
            key_parts = ['cache', key_prefix] + [func.__name__] + hashable_args
            key = ':'.join(key_parts)

            cached = connection.get(key)
            if cached is not None:
                return json.loads(cached, cls=decoder)
            
            value = func(*args)
            connection.set(key, json.dumps(value, cls=encoder), ttl)
            return value
        return wrapper
    return decorator
