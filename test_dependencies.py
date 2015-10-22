# coding=utf-8

import json
import unittest

from .instances import frontik_test_app


class TestDependencies(unittest.TestCase):
    def test_dependencies(self):
        response_json = frontik_test_app.get_page_json('dependencies')
        self.assertSetEqual(set(response_json['run_dependencies']), {'dep1', 'dep2', 'dep3', 'dep4'})
        self.assertEqual(response_json['dep1_value'], 'dep1_result')

    def test_exception(self):
        response = frontik_test_app.get_page('dependencies?fail=true')

        self.assertEquals(response.status_code, 403)
        self.assertEquals(json.loads(response.content), {'reason': 'failed in dependency'})
