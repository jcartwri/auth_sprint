from functools import wraps
from http import HTTPStatus
from typing import Any, Callable

import sqlalchemy.exc
from flask import request
from flask_jwt_extended import get_jwt_identity
from utils.jaeger import tracer
from utils.rate_limit import Bucket


def error_exceptions(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except KeyError:
            return {'message': 'Can\'t get access token cause of key error'}
        except sqlalchemy.exc.IntegrityError:
            return {'message': 'Can\'t add row to the table :('}
    return wrapper


def rate_limit():
    def rate_limit_decor(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_ident: str = get_jwt_identity()['identifier']
            bucket = Bucket(user_ident)
            res = bucket.algorithm()
            if not res:
                return {'message': 'Too Many Requests'}, HTTPStatus.TOO_MANY_REQUESTS
            return func(*args, **kwargs)
        return wrapper
    return rate_limit_decor


def tracing(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        request_id = request.headers.get('X-Request-Id')
        with tracer.start_span(name=fn.__name__) as span:
            span.set_attribute('http.request_id', request_id)
            return fn(*args, **kwargs)
    return decorated
