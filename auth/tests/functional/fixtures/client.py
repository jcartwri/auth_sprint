import asyncio

import aiohttp
import pytest
from tests.functional.settings import TestSettings
from tests.functional.utils import helper

settings = TestSettings()


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope='session', autouse=True)
async def delete_data(session):
    await helper.delete_all_data_from_tables(session, settings)
    yield
    await helper.delete_all_data_from_tables(session, settings)

