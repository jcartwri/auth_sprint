import pytest

from .settings import TestSettings

settings = TestSettings()
pytest_plugins = ["tests.functional.fixtures.client", "tests.functional.fixtures.load_data"]


@pytest.fixture(scope='session')
def make_get_request(session):
    async def inner(path: str, params: dict = None, headers: dict = None):
        params = params or {}
        url = '{protocol}://{host}:{port}/api/v1/{path}'.format(
            protocol='http',
            host=settings.service_host,
            port=settings.service_port,
            path=path
        )
        headers = headers or None
        async with session.get(url, params=params, headers=headers) as response:
            body = await response.json()
            status = response.status
            return body, status

    return inner


@pytest.fixture(scope='session')
def make_request(session):
    async def inner(req_type: str, path: str, json: dict = None, headers: dict = None):
        requests: dict = {"post": session.post, "get": session.get, "delete": session.delete}
        json = json or {}
        headers = headers or None
        async with requests[req_type](settings.AUTH_SERVICE_URL + path, json=json, headers=headers) as response:
            body = await response.json()
            status = response.status
            return body, status
    return inner
