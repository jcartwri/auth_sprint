from http import HTTPStatus

import pytest
import tests.functional.data.login as log
import tests.functional.data.protected as protect
import tests.functional.data.registration as reg
from tests.functional.utils.create_login import request_users


@pytest.mark.parametrize(
    'user_info, expected_answer',
    [
        (
                reg.user_wrong_password,
                {'status': HTTPStatus.BAD_REQUEST, 'body': reg.user_wrong_pwd_mess}
        ),
        (
                reg.user_wrong_email,
                {'status': HTTPStatus.BAD_REQUEST, 'body': reg.user_wrong_email_mess}
        ),
        (
                reg.user_missing_field,
                {'status': HTTPStatus.BAD_REQUEST, 'body': reg.user_missing_field_mess}
        ),
        (
                reg.user_correct,
                {'status': HTTPStatus.OK, 'body': reg.user_correct_mess}
        )
    ]
)
@pytest.mark.asyncio
async def test_registration(make_request, user_info, expected_answer):
    body, status = await make_request('post', 'registration', json=user_info)
    assert status == expected_answer['status']
    assert body == expected_answer['body']


@pytest.mark.parametrize(
    'user_info, expected_answer',
    [
        (
                log.user_not_ex,
                {'status': HTTPStatus.NOT_FOUND, 'body': log.user_not_ex_mess}
        ),
        (
                log.wrong_user_credentials,
                {'status': HTTPStatus.FORBIDDEN, 'body': log.wrong_user_credentials_mess}
        ),
        (
                log.user_login_ok,
                {'status': HTTPStatus.OK, 'body': log.user_login_ok_mess}
        )
    ]
)
@pytest.mark.asyncio
async def test_login(make_request, user_info, expected_answer):
    _, _ = await make_request('post', 'registration', json=reg.user_data_1)
    body, status = await make_request('post', 'login', json=user_info)

    assert status == expected_answer['status']

    if user_info == log.user_login_ok:
        assert len(body) == len(expected_answer['body'])
    else:
        assert body == expected_answer['body']


@pytest.mark.asyncio
async def test_access_token_protected_url(make_request):
    body, _, access_headers, _ = await request_users(make_request, reg.user_data_3)
    body, status = await make_request('get', 'protected', headers=access_headers)

    assert status == HTTPStatus.OK
    assert body == protect.correct_access_token

    wrong_headers = {"Authorization": "Bearer {0}".format(protect.wrong_token_signature)}
    body, status = await make_request('get', 'protected', headers=wrong_headers)

    assert status == HTTPStatus.FORBIDDEN
    assert body == protect.wrong_access_token


@pytest.mark.asyncio
async def test_logout(make_request):
    body, _, access_headers, _ = await request_users(make_request, reg.user_data_3)
    body, status = await make_request('post', 'logout', headers=access_headers)

    assert status == HTTPStatus.OK
    assert body == protect.TOKEN_REVOKED


@pytest.mark.asyncio
async def test_refresh(make_request):
    body, _, _, refresh_headers = await request_users(make_request, reg.user_data_3)
    body, status = await make_request('post', 'token/refresh', headers=refresh_headers)
    assert status == HTTPStatus.OK
