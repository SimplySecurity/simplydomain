from unittest import TestCase
from src import module_helpers
import json


class TestRequestsHelpers(TestCase):

    h = module_helpers.RequestsHelpers()

    def test_request_json(self):
        msg, val = self.h.request_json(
            'http://echo.jsontest.com/key1/key-val/key2/key-val2', return_code=200)
        if not val:
            self.fail()
        j = json.loads(msg)
        self.assertDictEqual({'key2': 'key-val2', 'key1': 'key-val'}, j)

    def test_request_content(self):
        msg, val = self.h.request_content('https://httpbin.org/ip')
        if not val:
            self.fail()
        j = json.loads(msg)

    def test_request_raw(self):
        r, val = self.h.request_raw('https://httpbin.org/ip')
        if not val:
            self.fail()
        j = json.loads(r.content)
