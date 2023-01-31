from functools import wraps

import requests
from core.config import AUTH_SERVICE_HOST, AUTH_SERVICE_PORT
from core.messages import PERMISSION_ERROR, TOKEN_INVALID
from fastapi import Request


def token_required(func):
    @wraps(func)
    async def wrapper(*args, request: Request, **kwargs):
        response = requests.get(f"http://{AUTH_SERVICE_HOST}:{AUTH_SERVICE_PORT}/get_username", headers=request.headers)

        if response and response.status_code != 200:
            kwargs["error"] = {
                "value": {
                    "message": "wrong data",
                    "errors": [{"name": TOKEN_INVALID}],
                },
            }
        elif response is None or not response.json().get("username", None):
            kwargs["error"] = {
                "value": {
                    "message": "wrong data",
                    "errors": [{"name": PERMISSION_ERROR}],
                },
            }

        return await func(*args, request, **kwargs)
    return wrapper