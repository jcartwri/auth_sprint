from http import HTTPStatus

import pytest
import tests.functional.data.change_password as pwd
from tests.functional.utils.create_login import request_users


@pytest.mark.parametrize(
    'user_info, expected_answer',
    [
        (
                pwd.uncorrect_pwd_data,
                {'status': HTTPStatus.FORBIDDEN, 'body': pwd.wrong_pwd}
        ),
        (
                pwd.correct_data,
                {'status': HTTPStatus.OK, 'body': pwd.ok_pwd}
        )
    ]
)
@pytest.mark.asyncio
async def test_change_password(make_request, user_info, expected_answer):
    _, _, access_headers, refresh_headers = await request_users(make_request, pwd.user_data_4)
    body, status = await make_request('post', 'update/password', json=user_info, headers=access_headers)

    assert status == expected_answer['status']
    assert body == expected_answer['body']
