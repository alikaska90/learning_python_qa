from srv.base_request import BaseRequest


def test_code_status(params):
    url, status_code = params
    base_request = BaseRequest(url)
    assert base_request.get().status_code == status_code
