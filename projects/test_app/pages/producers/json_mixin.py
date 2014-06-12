# coding=utf-8

from frontik.handler import HTTPError, PageHandler, JsonProducerMixin


class Page(PageHandler, JsonProducerMixin):
    def get_page(self):
        self.json.put({'json': True})
        self.doc.put('xml')
        self.text = 'text'

    def post_page(self):
        raise ValueError('Testing standard exception')

    def put_page(self):
        raise HTTPError(404, 'No way')
