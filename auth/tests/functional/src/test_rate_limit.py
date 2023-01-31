from http import HTTPStatus

import pytest
import tests.functional.data.rate_limit as rl
from tests.functional.utils.create_login import request_users


@pytest.mark.parametrize(
    'user_info, range_number, expected_answer',
    [
        (
                rl.user_data,
                19,
                {'status': HTTPStatus.OK, 'body': rl.okey_mess}
        ),
        (
                rl.user_data,
                21,
                {'status': HTTPStatus.TOO_MANY_REQUESTS, 'body': rl.rate_limit_mess}
        )
    ]
)
@pytest.mark.asyncio
async def test_change_password(make_request, user_info, range_number, expected_answer):
    global status

    body, _, access_headers, _ = await request_users(make_request, user_info)
    for _ in range(range_number):
        body, status = await make_request('get', 'protected', headers=access_headers)

    assert status == expected_answer['status']
    assert body == expected_answer['body']
