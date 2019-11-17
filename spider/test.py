# -*- coding: utf-8 -*-
from manager.engine import Engine


class Spider(Engine):
    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)

    def start_request(self):

        for i in range(100):
            # if i % 10 == 0:
            #     url = 'https://www.google.com'
            # else:
            url = 'https://www.aaabaidu.com'
            self.produce(url)

    def parse(self, res):
        import time
        time.sleep(3)
        print(res.status_code, 'done!')