# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import threading


class Request:
    def __init__(self, request, loop):
        self.request = request
        self.loop = loop
        self.connector = None

    async def quest(self, request):
        if request:
            self.request = request
        async with asyncio.Semaphore(200):
            if not self.connector:
                self.connector = aiohttp.TCPConnector(ssl=self.request.verify)
            if not self.request.session:
                session = aiohttp.ClientSession(connector=self.connector)
                self.request.session = session
            await asyncio.sleep(5)
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

    def runs_forever(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()


loop = asyncio.get_event_loop()

r = Request(type("request", (), {'method': 'get', 'url': 'http://www.baidu.com', 'verify': False, 'session': None}), loop)
tasks = []
thread = threading.Thread(target=r.runs_forever, args=(loop,))
thread.setDaemon(True)
thread.start()
f = []
for i in ['http://www.baidu.com', 'http://www.baidu.com/s?wd=hello', 'http://www.baidu.com/s?wd=xixi']:
    print('消费：', i)
    f.append(r.quest(type("request", (), {'method': 'get', 'url': i, 'verify': False, 'session': None})))
fs = asyncio.run_coroutine_threadsafe(asyncio.wait(f), loop)
print(list(map(lambda x: x.result(), list(fs.result()[0]))))

print()


asyncio.run_coroutine_threadsafe(r.request.session.close(), loop)
