from srv.base_request import BaseRequest
import pytest

from json_schemes.jesonplaceholder import JSON_SCHEMA
from srv.util import json_validation

BASE_URL = 'https://jsonplaceholder.typicode.com/posts'


@pytest.fixture(scope='module')
def api():
    yield BaseRequest(base_url=BASE_URL)


@pytest.mark.parametrize('resource_id',
                         [1, 3, 100])
def test_get_resource_positive(api, resource_id):
    resource = api.get(f'/{resource_id}')
    assert resource.status_code == 200
    body = api.get_body(resource)
    assert json_validation(body, JSON_SCHEMA)
    assert body['id'] == resource_id


@pytest.mark.parametrize('resource_id',
                         [0, 101])
def test_get_resource_negative(api, resource_id):
    resource = api.get(f'/{resource_id}')
    assert resource.status_code == 404
    assert resource.reason == 'Not Found'


def test_create_new_resource(api):
    data = {'title': 'foo',
            'body': 'bar',
            'userId': 1}
    new_resource = api.post(data=data)
    assert new_resource.status_code == 201
    body = api.get_body(new_resource)
    assert json_validation(body, JSON_SCHEMA)
    assert body['title'] == data['title']
    assert body['body'] == data['body']
    if isinstance(body['userId'], str):
        pytest.skip('BUG: returned userId has string type')
    assert body['userId'] == data['userId']


@pytest.mark.parametrize('resource_id',
                         [1])
def test_resource_update(api, resource_id):
    data = {'id': 1,
            'title': 'foo',
            'body': 'bar',
            'userId': 1}
    updated_resource = api.put(url=f'/{resource_id}', data=data)
    assert updated_resource.status_code == 200
    body = api.get_body(updated_resource)
    assert json_validation(body, JSON_SCHEMA)
    assert body['id'] == data['id']
    assert body['title'] == data['title']
    assert body['body'] == data['body']
    if isinstance(body['userId'], str):
        pytest.skip('BUG: returned userId has string type')
    assert body['userId'] == data['userId']


@pytest.mark.parametrize(('resource_id', 'data'),
                         [(1, {'title': 'foo'}),
                          (1, {'body': 'bar'}),
                          (1, {'title': 'foo', 'body': 'bar'})],
                         ids=['change title',
                              'change body',
                              'change title and body'])
def test_resource_patching(api, resource_id, data):
    origin_resource = api.get_body(api.get(url=f'/{resource_id}'))
    patched_resource = api.patch(url=f'/{resource_id}', data=data)
    for key in data.keys():
        origin_resource[key] = data[key]
    assert patched_resource.status_code == 200
    body = api.get_body(patched_resource)
    assert json_validation(body, JSON_SCHEMA)
    assert body == origin_resource


@pytest.mark.parametrize('resource_id',
                         [1])
def test_resource_delete(api, resource_id):
    deleted_resource = api.delete(url=f'/{resource_id}')
    assert deleted_resource.status_code == 200
