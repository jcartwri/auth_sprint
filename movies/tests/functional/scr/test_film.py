import json
from http import HTTPStatus

import pytest
import tests.functional.testdata.film_data as film
from tests.functional.utils.create_login import request_users


@pytest.mark.parametrize(
    'user_info, film_id, expected_answer',
    [
        (
                film.create_user_role_first,
                film.film_id,
                {'status': HTTPStatus.OK, 'body': film.film_id_res}
        ),
        (
                film.create_user_role_second,
                film.film_id_not_ex,
                {'status': HTTPStatus.NOT_FOUND, 'body': film.film_id_not_ex_res}
        ),
        (
                film.create_user_role_third,
                film.film_id,
                {'status': HTTPStatus.FORBIDDEN, 'body': film.permision_denied}
        )
    ]
)
@pytest.mark.asyncio
async def test_film(make_get_request, make_request, user_info, film_id, expected_answer):
    body, _, access_headers, _ = await request_users(make_request, user_info)
    _, _ = await make_request('post', 'role/create', json=user_info, headers=access_headers)
    _, _ = await make_request('post', 'add_user_role', json=user_info, headers=access_headers)

    body, status = await make_get_request('films/' + str(film_id), headers=access_headers)
    if body != expected_answer['body']:
        print("##################")
        print(body)
        print(expected_answer['body'])
    assert status == expected_answer['status']
    assert body == expected_answer['body']


@pytest.mark.asyncio
async def test_all_film(
        make_get_request,
        expected_answer=None
):
    if expected_answer is None:
        expected_answer = [
            {
                "id": i["id"],
                "title": i["title"],
                'imdb_rating': i['imdb_rating']
            } for i in film.film_data
        ]
    body, status = await make_get_request('films/?sort=imdb_rating%3Adesc&page[size]=50&page[number]=1')

    assert status == HTTPStatus.OK
    assert len(body) == len(expected_answer)

    for elem in body:
        assert elem in expected_answer


@pytest.mark.asyncio
async def test_film_page_wrong(make_get_request):
    body, status = await make_get_request('films/?sort=imdb_rating%3Adesc&page[size]=50&page[number]=0')
    assert status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_film_cache(make_get_request, redis_client):
    _, _ = await make_get_request('films/' + str(film.film_id))
    redis_key = "movies::guid::{id_}".format(id_=film.film_id)

    res = await redis_client.get(redis_key)
    res = json.loads(res.decode('utf8'))

    assert res['id'] == film.film_id
