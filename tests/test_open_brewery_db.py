from srv.base_request import BaseRequest
import pytest

from json_schemes.open_brewery_db import JSON_SCHEMA
from srv.util import wrong_elements, default_value_for_less_min_or_more_max, json_validation

BASE_URL = 'https://api.openbrewerydb.org/v1/breweries'


@pytest.fixture(scope='module')
def api():
    yield BaseRequest(base_url=BASE_URL)


@pytest.mark.parametrize('brewery_id',
                         ['b54b16e1-ac3b-4bff-a11f-f7ae9ddc27e0'])
def test_single_brewery_by_id_positive(api, brewery_id):
    brewery_by_id = api.get(f'/{brewery_id}')
    assert brewery_by_id.status_code == 200
    body = api.get_body(brewery_by_id)
    assert json_validation(body, JSON_SCHEMA['items'])
    assert body['id'] == brewery_id


@pytest.mark.parametrize('brewery_id',
                         ['b54b16e1-ac3b-4bff-a11f-f7ae9ddc27e0__'])
def test_single_brewery_by_id_negative(api, brewery_id):
    brewery_by_id = api.get(f'/{brewery_id}')
    assert brewery_by_id.status_code == 404
    body = api.get_body(brewery_by_id)
    assert body['message'] == "Couldn't find Brewery"


@pytest.mark.parametrize('params_dict',
                         [{'by_city': 'san_diego'},
                          {'by_city': 'san_diego', 'per_page': 3}],
                         ids=['breweries by city',
                              'breweries by city with count'])
def test_breweries_by_city(api, params_dict):
    brewery_by_city = api.get(params=params_dict)
    assert brewery_by_city.status_code == 200
    body = api.get_body(brewery_by_city)
    assert json_validation(body, JSON_SCHEMA)
    city_set = {brewery['city'] for brewery in body}
    wrong_cities = wrong_elements(city_set, params_dict['by_city'].replace('_', ' '), True)
    assert not wrong_cities, 'Wrong breweries in result'
    if 'per_page' in params_dict:
        assert len(body) == params_dict['per_page']


@pytest.mark.parametrize('params_dict',
                         [{},
                          {'size': 0},
                          {'size': 3},
                          {'size': 50},
                          {'size': 51}],
                         ids=['single random brewery',
                              'less then min num of random breweries',
                              '3 random breweries',
                              'max num of random breweries',
                              'more then max num of random breweries'])
def test_random_breweries(api, params_dict):
    random_breweries = api.get(url=f'/random', params=params_dict)
    assert random_breweries.status_code == 200
    body = api.get_body(random_breweries)
    assert json_validation(body, JSON_SCHEMA)
    num_of_breweries = 1
    if params_dict:
        num_of_breweries = default_value_for_less_min_or_more_max(1, 50, params_dict['size'])
    assert len(body) == num_of_breweries


@pytest.mark.parametrize(('operation', 'params_dict'),
                         [('search', {'query': 'dog', 'per_page': 3}),
                          ('autocomplete', {'query': 'dog'})])
def test_search_breweries(api, operation, params_dict):
    searched_breweries = api.get(url=f'/{operation}', params=params_dict)
    assert searched_breweries.status_code == 200
    body = api.get_body(searched_breweries)
    name_list = [brewery['name'] for brewery in body]
    wrong_names = wrong_elements(name_list, params_dict['query'], True)
    assert not wrong_names, 'Wrong breweries in result'
    if operation == 'search':
        assert json_validation(body, JSON_SCHEMA)
    if operation == 'autocomplete':
        assert len(body) <= 15
    if 'per_page' in params_dict:
        assert len(body) == params_dict['per_page']
