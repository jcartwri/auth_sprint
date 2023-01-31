from http import HTTPStatus

import pytest
import tests.functional.data.change_password as pwd
import tests.functional.data.page_info as page
from tests.functional.utils.create_login import request_users


# 2 тест - пагинация. 12 входов - 10 результатов на странице
@pytest.mark.parametrize(
    'page_number, user_data, expected_answer',
    [
        (
                page.page_not_found,
                pwd.user_data_page,
                {'status': HTTPStatus.NOT_FOUND, 'body': page.page_not_found_mess}
        ),
        (
                page.page_found,
                pwd.user_data_page,
                {'status': HTTPStatus.OK, 'body': page.page_found_len}
        )
    ]
)
@pytest.mark.asyncio
async def test_auth_history(make_request, page_number, user_data, expected_answer):
    _, _, access_headers, refresh_headers = await request_users(make_request, user_data)

    for _ in range(12):
        _, _ = await make_request('post', 'login', json=user_data)

    body, _ = await make_request('post', 'login', json=user_data)

    access_headers = {"Authorization": "Bearer {0}".format(body['access_token'])}
    body, status = await make_request('get', 'auth/history', json=page_number, headers=access_headers)

    assert status == expected_answer['status']

    if expected_answer['body'] == page.page_not_found_mess:
        assert body == expected_answer['body']
    else:
        assert len(body['history']) == 10
