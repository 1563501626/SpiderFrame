# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import threading


class Request:

    async def quest(self, session, method, url, ):
        async with asyncio.Semaphore(200):
            res, text = await self.__getattribute__(method)(session, url)
            return text, res

    @staticmethod
    async def new_session(verify=True):
        connector = aiohttp.TCPConnector(ssl=verify)
        session = aiohttp.ClientSession(connector=connector)
        return session

    @staticmethod
    async def get(session, request):
        async with session.get(request) as res:
            text = await res.read()
            return res, text

    @staticmethod
    async def exit(session):
        await session.close()

    @staticmethod
    def run_forever(loops):
        asyncio.set_event_loop(loops)
        loop.run_forever()

    @staticmethod
    def func(future):
        print(future.result())


r = Request()
loop = asyncio.new_event_loop()
sessions = loop.run_until_complete(r.new_session())
tasks = []
thread = threading.Thread(target=r.run_forever, args=(loop,))
thread.setDaemon(True)
thread.start()
f = []
# sess_loop = asyncio.new_event_loop()
# sessions = sess_loop.run_until_complete(r.new_session())
print()
for i in ['http://www.baidu.com', 'http://www.baidu.com/s?wd=hello', 'http://www.baidu.com/s?wd=xixi']:
    print('消费：', i)
    f.append(loop.create_task(r.quest(sessions, method='get', url=i)))
fs = asyncio.run_coroutine_threadsafe(asyncio.wait(f), loop)
ret = fs.add_done_callback(r.func)
print()
asyncio.run_coroutine_threadsafe(r.exit(sessions), loop)