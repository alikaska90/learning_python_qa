import json.decoder
import requests


class BaseRequest:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, url='', **kwargs):
        return requests.get(self.base_url+url, **kwargs)

    def post(self, url='', **kwargs):
        return requests.post(self.base_url+url, **kwargs)

    def put(self, url='', **kwargs):
        return requests.put(self.base_url+url, **kwargs)

    def patch(self, url='', **kwargs):
        return requests.patch(self.base_url+url, **kwargs)

    def delete(self, url='', **kwargs):
        return requests.delete(self.base_url+url, **kwargs)

    def get_body(self, response):
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            raise ValueError(f"Response isn't in format JSON. Response text: {response.text}")
