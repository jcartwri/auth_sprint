import abc
import datetime

from circuitbreaker import circuit
from database.redis_cache import redis_cache
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Реализация из коробки
limiter = Limiter(
    app, key_func=get_remote_address,
    storage_uri="redis://localhost:6379",
    default_limits=["10 per minute"],
    strategy="fixed-window",
)


# Пользовательская реализация
class RateLimiter:
    def __init__(self, cache, req_limit: int = 20, sec_limit: int = 59):
        """
        Requests' rate limiter.
        :param cache: Storage for tokens
        :param req_limit: Limit number for requests
        :param sec_limit: Limit seconds for requests
        """

        self.req_limit = req_limit
        self.cache = cache
        self.sec_limit = sec_limit

    @abc.abstractmethod
    def algorithm(self):
        pass


class Bucket(RateLimiter):
    @circuit
    def __init__(self, user_identifier: str):
        super().__init__(cache=redis_cache)
        self.user_identifier = user_identifier
        self.pipe = self.cache.pipeline()

    @circuit
    def algorithm(self):
        now = datetime.datetime.now()
        key = f'{self.user_identifier}:{now.minute}'
        request_number = self.cache.get(key)
        if request_number and int(request_number) > self.req_limit:
            return False
        pipe = self.cache.pipeline()
        pipe.incr(key, 1)
        pipe.expire(key, self.sec_limit)
        pipe.execute()
        return True
