from http import HTTPStatus

import pytest
import tests.functional.data.registration as reg
import tests.functional.data.role as data_role
from tests.functional.utils.create_login import request_users


@pytest.mark.parametrize(
    'user_info, expected_answer',
    [
        (
                data_role.test_role_create,
                {'status': HTTPStatus.OK, 'body': data_role.test_role_create_mess}
        ),
        (
                data_role.false_test_role_create,
                {'status': HTTPStatus.BAD_REQUEST, 'body': data_role.false_test_role_create_mess}
        )
    ]
)
@pytest.mark.asyncio
async def test_create_role(make_request, user_info, expected_answer):
    body, _, access_headers, _ = await request_users(make_request, reg.user_data_3)
    body, status = await make_request('post', 'role/create', json=user_info, headers=access_headers)

    assert status == expected_answer['status']
    assert body == expected_answer['body']

    _, _ = await make_request('delete', 'role/delete', json=user_info, headers=access_headers)


@pytest.mark.parametrize(
    'user_info, expected_answer',
    [
        (
                data_role.test_role_delete,
                {'status': HTTPStatus.OK, 'body': data_role.test_role_delete_mess}
        )
    ]
)
@pytest.mark.asyncio
async def test_delete_role(make_request, user_info, expected_answer):
    _, _, access_headers, _ = await request_users(make_request, reg.user_data_3)
    _, _ = await make_request('post', 'role/create', json=user_info, headers=access_headers)
    body, status = await make_request('delete', 'role/delete', json=user_info, headers=access_headers)

    assert status == expected_answer['status']
    assert body == expected_answer['body']


@pytest.mark.parametrize(
    'user_info, expected_answer, create_role_for_change',
    [
        (
                data_role.test_role_change,
                {'status': HTTPStatus.OK, 'body': data_role.test_role_change_mess},
                data_role.create_role_for_change_test1
        ),
        (
                data_role.false_test_role_change,
                {'status': HTTPStatus.BAD_REQUEST, 'body': data_role.false_test_role_change_mess},
                data_role.create_role_for_change_test1
        )
    ]
)
@pytest.mark.asyncio
async def test_change_role(make_request, user_info, expected_answer, create_role_for_change):
    body, _, access_headers, _ = await request_users(make_request, reg.user_data_3)
    _, _ = await make_request('post', 'role/create', json=create_role_for_change, headers=access_headers)
    body, status = await make_request('post', 'role/change', json=user_info, headers=access_headers)

    assert status == expected_answer['status']
    assert body == expected_answer['body']

    _, _ = await make_request('delete', 'role/delete', json=create_role_for_change, headers=access_headers)
