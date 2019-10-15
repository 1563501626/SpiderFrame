import aiohttp
import asyncio


async def req(url, method, headers, data=None):
    async with asyncio.Semaphore(10):
        con = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=con) as sess:
            if method.upper() == 'GET':
                async with sess.get(url, headers=headers) as res:
                    content = await res.read()
            else:
                async with sess.post(url, headers=headers, data=data) as res:
                    content = await res.read()

    return content


def callback(future):
    print(future)
    print('done!')


# url = 'https://www.liaoxuefeng.com/wiki/1016959663602400/1017970488768640'
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
# loop = asyncio.get_event_loop()
# # loop.run_until_complete(asyncio.wait([req(url, 'get', headers)]))
# task = loop.create_task(req(url, 'get', headers))
# task.add_done_callback(callback)
# loop.run_until_complete(task)
# print(task.result())
# loop.close()

async def apost(headers={}, data=None, **kw):
    session = aiohttp.ClientSession()
    await session.close()
    print()
loop = asyncio.get_event_loop()
loop.run_until_complete(apost())
loop.close()