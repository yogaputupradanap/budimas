import hashlib
import json

import redis
from flask import request


class RedisAutoCache:
    def __init__(self, host='localhost', port=6379, db=0, expire_time=300):
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True
        )
        self.expire_time = expire_time

    def _generate_cache_key(self, path, args):
        query_params = '&'.join(sorted([
            f"{k}={v}" for k, v in args.items()
        ]))
        key_base = f"{path}?{query_params}" if query_params else path
        return f"cache:{hashlib.md5(key_base.encode()).hexdigest()}"

    def _clear_all_cache(self):
        pattern = f"cache:*"
        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)

    def auto_cache(self, response):
        if request.method == 'GET' or request.method == 'OPTIONS':
            cache_key = self._generate_cache_key(request.path, request.args)
            try:
                json_response = response.get_json()
                if json_response:
                    self.redis_client.setex(
                        cache_key,
                        self.expire_time,
                        json.dumps(json_response)
                    )
            except:
                pass
            return response
        else:
            self._clear_all_cache()
            return response

    def check_cache(self):
        if request.method == 'GET' or request.method == 'OPTIONS':
            cache_key = self._generate_cache_key(request.path, request.args)
            cached_response = self.redis_client.get(cache_key)
            if cached_response:
                return json.loads(cached_response)
        return None
