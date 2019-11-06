# -*- coding: utf-8 -*-
from manager.engine import Engine


class Spider(Engine):
    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)

    def start_request(self):
        url = 'http://baidu.com'
        for i in range(100):
            self.produce(url)

    def parse(self, res):
        print(res.status_code, 'done!')