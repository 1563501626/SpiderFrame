# -*- coding: utf-8 -*-
import aiohttp, asyncio


async def quest(url, session=None):
    async with asyncio.Semaphore(200):
        if not session:
            session = aiohttp.ClientSession()
        res = await session.get(url)
        return session, await res.read()

loop = asyncio.get_event_loop()

tasks = []
session = ''
for i in ['http://www.baidu.com', 'http://www.baidu.com/s?wd=hello', 'http://www.baidu.com/s?wd=xixi']:
    s, _ = loop.run_until_complete(quest(i, session))
    if not session:
        session = s
    # tasks.append(session.get(i))
# print(loop.run_until_complete(asyncio.wait(tasks)))
loop.run_until_complete(session.close())
loop.close()