# coding=utf-8

import unittest

from .instances import frontik_test_app


class TestNonDebugMode(unittest.TestCase):
    def test_simple_types(self):
        result = frontik_test_app.get_page_json(
            'parse_arguments?str=str_value&int=100&bool=true&float=0.5&required='
        )

        self.assertEqual(result['str'], 'str_value')
        self.assertEqual(result['int'], 100)
        self.assertEqual(result['float'], 0.5)
        self.assertEqual(result['bool'], True)

    def test_defaults(self):
        result = frontik_test_app.get_page_json('parse_arguments?required=')

        self.assertEqual(result['bool'], False)
        self.assertEqual(result['str'], 'str_default')
        self.assertEqual(result['int'], 123456)
        self.assertEqual(result['float'], 1.2)
        self.assertEqual(result['list'], ['list_default'])

    def test_no_default(self):
        response = frontik_test_app.get_page('parse_arguments')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, '{"error": "parameter \\"required\\" is missing"}')

    def test_list_type(self):
        result = frontik_test_app.get_page_json(
            'parse_arguments/list_types?str=t1&str=t2&int=1&float=1&float=2.0&float=3&bool=false'
        )

        self.assertEqual(result['bool'], [False])
        self.assertEqual(result['str'], ['t1', 't2'])
        self.assertEqual(result['int'], [1])
        self.assertEqual(result['float'], [1.0, 2.0, 3.0])
        self.assertEqual(result['str_empty'], [])

    def test_invalid_list_type(self):
        response = frontik_test_app.get_page('parse_arguments/list_types?int=1&int=test')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content, '{"error": "parameter \\"int\\" must be of type [int]"}'
        )

    def test_empty_list_type(self):
        response = frontik_test_app.get_page('parse_arguments/list_types?check_empty=true')
        self.assertEqual(response.status_code, 500)

    def test_choice_type(self):
        result = frontik_test_app.get_page_json('parse_arguments/choice?str=t1')
        self.assertEqual(result['str'], 't1')

        response = frontik_test_app.get_page('parse_arguments/choice?str=t4')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content, '{"error": "parameter \\"str\\" must be one of the following: (\'t1\', \'t2\', \'t3\')"}'
        )

    def test_choice_type_default_on_exception(self):
        result = frontik_test_app.get_page_json('parse_arguments/choice?str=t1&int=4')
        self.assertEqual(result['int'], 1)

    def test_invalid_arguments(self):
        response = frontik_test_app.get_page('parse_arguments?int=test&required=')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content, '{"error": "parameter \\"int\\" must be of type int"}'
        )

    def test_default_on_exception(self):
        result = frontik_test_app.get_page_json('parse_arguments?float=test&required=')
        self.assertEqual(result['float'], 1.2)

    def test_no_default_with_default_on_exception(self):
        response = frontik_test_app.get_page('parse_arguments?check_default_on_exception=true&required=')
        self.assertEqual(response.status_code, 500)
