# coding=utf-8

import frontik.handler


class Page(frontik.handler.PageHandler):
    def get_page(self):
        args = self.parse_arguments({
            'required': Page.Arg(str),
            'bool': Page.Arg(bool, default=False),
            'str': Page.Arg(str, default='str_default'),
            'int': Page.Arg(int, default=123456),
            'float': Page.Arg(float, default=1.2, default_on_exception=True),
            'list': Page.Arg([str], default=['list_default'])
        })

        if self.get_argument('check_default_on_exception', 'false') == 'true':
            self.parse_arguments({'no_default': Page.Arg(str, default_on_exception=True)})

        self.json.put({
            'required': args['required'],
            'bool': args['bool'],
            'str': args['str'],
            'int': args['int'],
            'float': args['float'],
            'list': args['list']
        })

    def write_error(self, status_code=500, **kwargs):
        if 'exc_info' in kwargs:
            exception = kwargs['exc_info'][1]
        else:
            exception = None

        if exception is not None:
            self.json.put({'error': exception.log_message})
            self.finish_with_postprocessors()
        else:
            super(Page, self).write_error(status_code, **kwargs)
