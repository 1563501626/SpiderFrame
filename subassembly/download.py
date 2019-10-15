# -*- coding: utf-8 -*-
import aiohttp


class Download:
    """下载网页信息"""

    def __init__(self, request, async_num=1):
        self.request = request
        self.async_num = async_num

    async def request(self):
        pass
