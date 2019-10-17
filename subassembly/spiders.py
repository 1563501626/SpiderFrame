# -*- coding: utf-8 -*-
import asyncio
import aiohttp


class Request:
    def __init__(self, request, loop):
        self.request = request
        self.loop = loop
        self.connector = None

    async def quest(self, request):
        if request:
            self.request = request
        async with asyncio.Semaphore(200):
            self.connector = aiohttp.TCPConnector(verify_ssl=self.request.verify)
            if self.request.session:
                session = self.request.session
            else:
                session = aiohttp.ClientSession(connector=self.connector)
                self.request.session = session
            res = await session.get(self.request.url)
            return await res.read()

    async def get(self):
        return await self.request.session.get(self.request.url)

    async def exit(self):
        await self.request.session.close()
        # await self.connector.close()

    def make_tasks(self, request=None):
        return self.loop.create_task(self.quest(request))

    def run(self, tasks):
        print(self.loop.run_until_complete(asyncio.wait(tasks)))


loop = asyncio.get_event_loop()
r = Request(type("request", (), {'method': 'get', 'url': 'http://www.baidu.com', 'verify': False, 'session': None}), loop)
tasks = []
for i in ['http://www.baidu.com', 'http://www.baidu.com/s?wd=hello', 'http://www.baidu.com/s?wd=xixi']:
    tasks.append(r.quest(type("request", (), {'method': 'get', 'url': i, 'verify': False, 'session': None})))
loop.run_until_complete(asyncio.wait(tasks))
loop.run_until_complete(r.request.session.close())
loop.close()