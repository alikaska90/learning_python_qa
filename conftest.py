import pytest


def pytest_addoption(parser):
    parser.addoption("--url", default="https://ya.ru/", type=str)
    parser.addoption("--status_code", default=200, type=int)


@pytest.fixture()
def params(request):
    return (request.config.getoption("--url"),
            request.config.getoption("--status_code"))
