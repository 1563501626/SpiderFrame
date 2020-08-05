# -*- coding: utf-8 -*-
import aiohttp
import chardet
import asyncio
import parsel
from urllib.parse import urljoin

from tools.exception import MyException
import logging

logger = logging.getLogger(__name__)


class Response:
    def __init__(self, url, content=None, status_code=None, charset=None, cookies=None, method=None,
                 headers=None, callback="parse", proxies=None, meta=None, res=None):
        self.url = url
        self.content = content
        self.status_code = status_code
        self.charset = charset
        self.cookies = cookies
        self.method = method
        self.headers = headers
        self.callback = callback
        self.proxies = proxies
        self.meta = meta
        self.res = res
        self.text = self._parse_content(charset, content)

    @staticmethod
    def _parse_content(charset, content):
        if not content:
            return
        if charset:
            try:
                text = content.decode(charset)
            except UnicodeDecodeError:
                try:
                    char = chardet.detect(content)
                    if char:
                        text = content.decode(char['encoding'])
                    else:
                        raise UnicodeDecodeError
                except UnicodeDecodeError:
                    try:
                        text = content.decode('utf-8')
                    except UnicodeDecodeError:
                        try:
                            text = content.decode("GBK")
                        except UnicodeDecodeError:
                            text = content.decode('utf-8', "ignore")
        else:
            try:
                text = content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    char = chardet.detect(content)
                    if char:
                        text = content.decode(char)
                    else:
                        raise UnicodeDecodeError
                except UnicodeDecodeError:
                    try:
                        text = content.decode('gb2312')
                    except UnicodeDecodeError:
                        text = content.decode('utf-8', "ignore")
        return text

    def xpath(self, x):
        r = parsel.Selector(self.text)
        return r.xpath(x)

    def css(self, x):
        r = parsel.Selector(self.text)
        return r.css(x)

    def urljoin(self, url):
        return urljoin(self.url, url)


class Retry:
    def __init__(self):
        self.func = None

    async def run(self, session, request, init_max_times):
        retry_times = 0
        max_times = init_max_times
        while max_times:
            try:
                return await self.func(session, request, init_max_times)
            except asyncio.TimeoutError:
                logger.info("第%s次请求超时，url：{%s}" % (retry_times, request['url']))
                retry_times += 1
                max_times -= 1
            except MyException as e:
                raise e
            except Exception as e:
                logger.info("第%s次请求报错{%s}，url：{%s}" % (retry_times, e, request['url']))
                retry_times += 1
                max_times -= 1

    def __call__(self, func):
        self.func = func
        return self.run


class Request:
    @staticmethod
    @Retry()
    async def quest(session, request, max_times):
        if request['method'].upper() == 'GET':
            async with session.get(request['url'], params=request['params'], cookies=request['cookies'],
                                   headers=request['headers'], proxy=request['proxies'],
                                   allow_redirects=request['allow_redirects'], timeout=request['time_out']) as res:
                text = await res.read()

        elif request['method'].upper() == 'POST':
            async with session.post(request['url'], data=request['data'], json=request['json'],
                                    cookies=request['cookies'],
                                    headers=request['headers'], proxy=request['proxies'],
                                    allow_redirects=request['allow_redirects']) as res:
                text = await res.read()
        else:
            raise MyException("{%s}请求方式未定义，请自定义添加！" % request['method'])

        if res:
            status_code = res.status
            charset = res.charset
            response = Response(request['url'], text, status_code, charset, request['cookies'], request['method'],
                                request['headers'], request['callback'], request['proxies'], request['meta'], res)
            return response

    @staticmethod
    async def new_session(verify=True):
        connector = aiohttp.TCPConnector(ssl=verify)
        session = aiohttp.ClientSession(connector=connector)
        return session

    @staticmethod
    async def get(session, request):
        async with session.get(request['url'], params=request['params'], cookies=request['cookies'],
                               headers=request['headers'], proxy=request['proxies'],
                               allow_redirects=request['allow_redirects'], timeout=request['time_out']) as res:
            text = await res.read()
            return res, text

    @staticmethod
    async def post(session, request):
        async with session.post(request['url'], data=request['data'], json=request['json'], cookies=request['cookies'],
                                headers=request['headers'], proxy=request['proxies'],
                                allow_redirects=request['allow_redirects']) as res:
            text = await res.read()
            return res, text

    @staticmethod
    async def exit(session):
        await session.close()

    @staticmethod
    def func(future):
        logger.info(future.result())
        return future.result()
