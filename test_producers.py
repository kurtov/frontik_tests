import json
import unittest

import requests

from .instances import frontik_test_app


class TestNonDebugMode(unittest.TestCase):
    def test_content_type(self):
        response = frontik_test_app.get_page('producers/json_mixin')
        self.assertEqual(response.content, '{"json": true}')

    def test_standard_exception(self):
        response = frontik_test_app.get_page('producers/json_mixin', method=requests.post)
        self.assertEqual(response.status_code, 500)

        data = json.loads(response.content)
        self.assertEqual(data['error'], True)
        self.assertEqual(data['status_code'], 500)
        self.assertEqual(data['message'], 'Testing standard exception')

    def test_http_error(self):
        response = frontik_test_app.get_page('producers/json_mixin', method=requests.put)
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.content)
        self.assertEqual(data['error'], True)
        self.assertEqual(data['status_code'], 404)
        self.assertEqual(data['message'], 'No way')
