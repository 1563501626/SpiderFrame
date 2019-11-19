import aiohttp
import asyncio
import threading


async def req(url, method='GET', headers='', data=None):
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


def forever(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def aa(url):
    return await req(url)


url = 'https://www.liaoxuefeng.com/wiki/1016959663602400/1017970488768640'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
loop = asyncio.get_event_loop()
t = threading.Thread(target=forever, args=(loop, ))
t.setDaemon(True)
t.start()
ret = asyncio.run_coroutine_threadsafe(aa('https://baidu.com'), loop)
print(ret.result())

async def apost(headers={}, data=None, **kw):
    session = aiohttp.ClientSession()
    await session.close()
    print()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(apost())
# loop.close()
