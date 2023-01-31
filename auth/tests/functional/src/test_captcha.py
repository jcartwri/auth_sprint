from http import HTTPStatus

import pytest
import tests.functional.data.captcha as data_captcha
from tests.functional.utils.create_login import request_users


@pytest.mark.parametrize(
    'user_info,expected_answer',
    [
        (
                data_captcha.captcha_create_query_success,
                {'status': HTTPStatus.OK, 'body': data_captcha.captcha_create_answear_success}
        ),
    ]
)
@pytest.mark.asyncio
async def test_create_captcha(make_request, user_info, expected_answer):
    body, _, access_headers, _ = await request_users(make_request, user_info)
    _, _ = await make_request('post', 'role/create', json=user_info, headers=access_headers)
    _, _ = await make_request('post', 'add_user_role', json=user_info, headers=access_headers)

    body, status = await make_request('post', 'captcha/create', json=user_info, headers=access_headers)

    assert status == expected_answer['status']
    assert type(body) == str


@pytest.mark.parametrize(
    'user_info,expected_answer',
    [
        (
                data_captcha.captcha_create_query_success,
                {"status": HTTPStatus.OK, "body": {"value": data_captcha.captcha_check_answear_success}}
        ),
        (
                data_captcha.captcha_create_query_fail,
                {"status": HTTPStatus.FORBIDDEN, "body": {"value": data_captcha.captcha_check_answear_fail}}
        ),
    ]
)
@pytest.mark.asyncio
async def test_check_captcha(make_request, user_info, expected_answer):
    body, _, access_headers, _ = await request_users(make_request, user_info)
    _, _ = await make_request('post', 'role/create', json=user_info, headers=access_headers)
    _, _ = await make_request('post', 'add_user_role', json=user_info, headers=access_headers)
    _, _ = await make_request('post', 'captcha/create', json=user_info, headers=access_headers)

    body, status = await make_request('post', 'captcha/check', json=user_info, headers=access_headers)

    assert status == expected_answer['status']
    assert body == expected_answer["body"]
