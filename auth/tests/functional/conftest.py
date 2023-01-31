import pytest

from .settings import TestSettings

settings = TestSettings()

pytest_plugins = ["tests.functional.fixtures.client"]


@pytest.fixture(scope='session')
def make_request(session):
    async def inner(req_type: str, path: str, json: dict = None, headers: dict = None):
        requests: dict = {"post": session.post, "get": session.get, "delete": session.delete}
        json = json or {}
        headers = headers or None
        async with requests[req_type](settings.SERVICE_URL + path, json=json, headers=headers) as response:
            body = await response.json()
            status = response.status
            return body, status
    return inner
