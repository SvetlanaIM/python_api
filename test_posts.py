import pytest
import requests
import pytest_check as check
from .validation.validator import validate
from .validation.schema import schema

base_url = "https://jsonplaceholder.typicode.com/posts"


@pytest.mark.parametrize(
    'endpoint, expected_code',
    [
        ('/1', 200),
        ('/0', 404),
        ('/100', 200),
        ('/101', 404),
        ('/99', 200)
    ])
def test_get_post(endpoint, expected_code):
    response = requests.get(base_url + endpoint)
    actual_code = response.status_code
    assert actual_code == expected_code, f'Check endpoint /posts{endpoint} as ' \
                                         f'expected status code is {expected_code}, actual - {actual_code}'


@pytest.mark.parametrize(
    'params, expected_code',
    [
        ({"userId": 1}, 200),
        ({"userId": 10}, 200),
        ({"userId": 11}, 404),
        ({"userId": 0}, 404),
        ({"userId": "foo"}, 404),
        ({"userId": - 1}, 404)
    ])
def test_filter_by_user_id(params, expected_code):
    response = requests.get(base_url, params=params)
    actual_code = response.status_code
    expected_user_id = params["userId"]
    assert actual_code == expected_code, f'Check /posts?userId={expected_user_id} as ' \
                                         f'expected status code is {expected_code}, actual - {actual_code}'
    for posts in response.json():
        assert posts["userId"] == expected_user_id, f'Filter shows irrelevant data'


def test_filter_by_two_parameters():
    params = {"userId": 1, "id": 4}
    response = requests.get(base_url, params=params)
    assert response.status_code == 200
    assert response.json()[0]["userId"] == params["userId"]
    assert response.json()[0]["id"] == params["id"]
    assert response.json()[0]["title"] == "eum et est occaecati"


def test_get_all_posts():
    response = requests.get(base_url)
    actual_code = response.status_code
    expected_code = 200
    actual_headers_info = response.headers["Content-Type"]
    expected_headers_info = "application/json; charset=utf-8"
    assert actual_code == expected_code, f'Actual response code is {actual_code}, expected {expected_code}'
    assert actual_headers_info == expected_headers_info, f'Actual response format ' \
                                                         f'is {actual_headers_info}, {expected_headers_info}'
    assert validate(response.json(), schema) is not "error", "Data does not match jsonschema"


@pytest.mark.parametrize(
    "data, expected_code",
    [
        ({"userId": "1", "title": "foo", "body": "bar"}, 201),
        ({"userId": "10", "title": "foo", "body": "bar"}, 201),
        ({"userId": "11", "title": "foo", "body": "bar"}, 400),  # non-existing user
        ({}, 400),
        ({"userId": "1"}, 400)
    ])
def test_create_post(data, expected_code):
    response = requests.post(base_url, data=data)
    actual_code = response.status_code
    assert actual_code == expected_code, f'Check status code: expected {expected_code}, ' \
                                         f'actual - {actual_code}'
    check.equal(response.json()["userId"], data["userId"], "userId is not as created")
    check.equal(response.json()["title"], data["title"], "title is not as created")
    check.equal(response.json()["body"], data["body"], "body is not as created")
    assert validate(response.json(), schema) is not "error", "Data does not match jsonschema"


@pytest.mark.parametrize(
    "endpoint, expected_code",
    [
        ("/1", 200),
        ("/100", 200),
        ("/0", 404),
        ("/101", 404)
    ])
def test_delete_post(endpoint, expected_code):
    response = requests.delete(base_url + endpoint)
    actual_code = response.status_code
    assert actual_code == expected_code, f'Check endpoint /posts{endpoint} ' \
                                         f'as expected status code is {expected_code}, actual - {actual_code}'
