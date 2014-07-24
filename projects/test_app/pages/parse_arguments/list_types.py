# coding=utf-8

from . import Page as ParentPage


class Page(ParentPage):
    def get_page(self):
        args = self.parse_arguments({
            'str': Page.Arg([str]),
            'str_empty': Page.Arg([str]),
            'int': Page.Arg([int]),
            'float': Page.Arg([float]),
            'bool': Page.Arg([bool])
        })

        if self.get_argument('check_empty', 'false') == 'true':
            self.parse_arguments({'empty': Page.Arg([])})

        self.json.put({
            'str': args['str'],
            'str_empty': args['str_empty'],
            'int': args['int'],
            'float': args['float'],
            'bool': args['bool']
        })
