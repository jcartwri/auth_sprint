from http import HTTPStatus

import pytest
import tests.functional.data.role as data_role
import tests.functional.data.user_role as data_user_role
from tests.functional.utils.create_login import request_users


@pytest.mark.parametrize(
    'user,user_info,role,expected_answer',
    [
        (
                data_user_role.user_correct,
                data_user_role.test_add_user_role,
                data_role.test_role_create,
                {'status': HTTPStatus.OK, 'body': data_user_role.test_add_user_role_answear}
        ),
        (
                data_user_role.user_correct_1,
                data_user_role.test_false_add_user_role,
                data_role.test_role_create_1,
                {'status': HTTPStatus.BAD_REQUEST, 'body': data_user_role.test_false_add_user_role_answear}
        )
    ]
)
@pytest.mark.asyncio
async def test_add_user_role(make_request, user, user_info, role, expected_answer):
    body, _, access_headers, _ = await request_users(make_request, user)

    _, _ = await make_request('post', 'role/create', json=role, headers=access_headers)
    body, status = await make_request('post', 'add_user_role', json=user_info, headers=access_headers)

    assert status == expected_answer['status']
    assert body == expected_answer['body']

    _, _ = await make_request('delete', 'role/delete', json=role, headers=access_headers)


@pytest.mark.parametrize(
    'user,user_info,role,expected_answer',
    [
        (
                data_user_role.user_correct_del,
                data_user_role.test_add_user_role_del,
                data_role.test_role_create_del,
                {'status': HTTPStatus.OK, 'body': data_user_role.test1_delete_user_role_answer_del}
        ),
        (
                data_user_role.user_correct_1,
                data_user_role.test_false_add_user_role,
                data_role.test_role_create_1,
                {'status': HTTPStatus.BAD_REQUEST, 'body': data_user_role.test2_delete_user_role_answear}
        )
    ]
)
@pytest.mark.asyncio
async def test_add_user_role_del(make_request, user, user_info, role, expected_answer):
    body, _, access_headers, _ = await request_users(make_request, user)

    _, _ = await make_request('post', 'role/create', json=role, headers=access_headers)
    _, _ = await make_request('post', 'add_user_role', json=user_info, headers=access_headers)
    body, status = await make_request('delete', 'delete_user_role', json=user_info, headers=access_headers)

    assert status == expected_answer['status']
    assert body == expected_answer['body']
