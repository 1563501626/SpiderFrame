# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import threading


class Request:
    def __init__(self, request, loop):
        self.request = request
        self.loop = loop
        self.connector = None

    def mk_session(self):
        self.connector = aiohttp.TCPConnector(ssl=self.request.verify)
        session = aiohttp.ClientSession(connector=self.connector)
        self.request.session = session

    async def quest(self, request):
        if request:
            self.request = request
        async with asyncio.Semaphore(200):
            await asyncio.sleep(2)
            res = await self.__getattribute__(self.request.method)()
            return await res.read(), res

    async def get(self):
        return await self.request.session.get(self.request.url)

    @staticmethod
    async def get_tasks(coroutine):
        return await asyncio.create_task(coroutine)

    async def exit(self):
        await self.request.session.close()
        await self.connector.close()

    def run_forever(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()


loop = asyncio.new_event_loop()
request = type("request", (), {'method': 'get', 'url': 'http://www.baidu.com', 'verify': False, 'session': None})
r = Request(request, loop)
r.mk_session()
tasks = []
thread = threading.Thread(target=r.run_forever, args=(loop,))
thread.setDaemon(True)
thread.start()
f = []
for i in ['http://www.baidu.com', 'http://www.baidu.com/s?wd=hello', 'http://www.baidu.com/s?wd=xixi']:
    print('消费：', i)
    f.append(r.quest()))
fs = asyncio.run_coroutine_threadsafe(asyncio.wait(f), loop)
print(list(map(lambda x: x.result(), list(fs.result()[0]))))
print()
asyncio.run_coroutine_threadsafe(r.request.session.close(), loop)
