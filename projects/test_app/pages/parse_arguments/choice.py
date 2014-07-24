# coding=utf-8

from . import Page as ParentPage


class Page(ParentPage):
    def get_page(self):
        args = self.parse_arguments({
            'str': Page.Arg(str, choice=('t1', 't2', 't3')),
            'int': Page.Arg(int, choice=(1, 2, 3), default=1, default_on_exception=True)
        })

        self.json.put({
            'str': args['str'],
            'int': args['int']
        })
