from json_schemes.dog_ceo_api import JSON_SCHEMA_SEVERAL_ITEMS, JSON_SCHEMA_ONE_ITEM, JSON_SCHEMA_ALL_BREEDS
from srv.base_request import BaseRequest
import pytest

from srv.util import wrong_elements, default_value_for_less_min_or_more_max, json_validation

BASE_URL = 'https://dog.ceo/api'


@pytest.fixture(scope='module')
def api():
    yield BaseRequest(base_url=BASE_URL)


def test_list_all_breeds(api):
    all_breeds = api.get('/breeds/list/all')
    assert all_breeds.status_code == 200
    body = api.get_body(all_breeds)
    assert json_validation(body, JSON_SCHEMA_ALL_BREEDS)
    assert body['status'] == 'success'


@pytest.mark.parametrize('breed',
                         ['hound', 'collie'],
                         ids=['test for hound',
                              'test for collie'])
def test_all_images_by_breed(api, breed):
    images_by_breed = api.get(f'/breed/{breed}/images')
    assert images_by_breed.status_code == 200
    body = api.get_body(images_by_breed)
    assert json_validation(body, JSON_SCHEMA_SEVERAL_ITEMS)
    assert body['status'] == 'success'
    message = body['message']
    wrong_images = wrong_elements(message, breed)
    assert not wrong_images, 'Wrong images in response'


@pytest.mark.parametrize(('breed', 'sub_breed'),
                         [('hound', 'afghan'),
                          ('cattledog', 'australian')],
                         ids=['test for hound-afghan',
                              'test for cattledog-australian'])
def test_all_images_by_sub_breed(api, breed, sub_breed):
    images_by_sub_breed = api.get(f'/breed/{breed}/{sub_breed}/images')
    assert images_by_sub_breed.status_code == 200
    body = api.get_body(images_by_sub_breed)
    assert json_validation(body, JSON_SCHEMA_SEVERAL_ITEMS)
    assert body['status'] == 'success'
    message = body['message']
    wrong_images = wrong_elements(message, f'{breed}-{sub_breed}')
    assert not wrong_images, 'Wrong images in response'


def test_random_image(api):
    random_image = api.get('/breeds/image/random')
    assert random_image.status_code == 200
    body = api.get_body(random_image)
    assert json_validation(body, JSON_SCHEMA_ONE_ITEM)
    assert body['status'] == 'success'
    assert isinstance(body['message'], str)
    assert 'https://images.dog.ceo/breeds/' in body['message']


@pytest.mark.parametrize('count_images',
                         [3, 50, 51, 0],
                         ids=['3 images',
                              'return max images',
                              'more then max images',
                              'less then min images'])
def test_random_images_with_count(api, count_images):
    random_images = api.get(f'/breeds/image/random/{count_images}')
    assert random_images.status_code == 200
    body = api.get_body(random_images)
    assert json_validation(body, JSON_SCHEMA_SEVERAL_ITEMS)
    assert body['status'] == 'success'
    assert isinstance(body['message'], list)
    count_images = default_value_for_less_min_or_more_max(1, 50, count_images)
    assert len(body['message']) == count_images
