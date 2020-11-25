# -*- coding: utf-8 -*-
import aiohttp
import chardet
import asyncio
import fuclib
import parsel
from urllib.parse import urljoin
from yarl import URL
from w3lib.encoding import (html_to_unicode, http_content_type_encoding)
import json as js

from tools.exception import MyException
import logging

logger = logging.getLogger(__name__)


class Response:
    def __init__(self, url, content=None, status_code=None, charset=None, cookies=None, method=None,
                 headers=None, callback="parse", proxies=None, meta=None, res=None):
        if meta is None:
            meta = {}
        self.url = url
        self.body = self.content = content
        self.status = self.status_code = status_code
        self.charset = charset
        self.res = res
        self.cookies = {k: v.value for k, v in self.res.cookies.items()}
        self.method = method
        self.headers = headers
        self.callback = callback
        self.proxies = proxies
        self.meta = meta if meta else {}

    def __str__(self):
        return self.text

    @property
    def text(self):
        if not self.content:
            return
        if self.charset:
            try:
                text = self.content.decode(self.charset)
            except UnicodeDecodeError:
                try:
                    benc = http_content_type_encoding(dict(self.res.headers)['Content-Type'])
                    if benc:
                        charset = 'charset=%s' % benc
                        text = html_to_unicode(charset, self.body)[1]
                    else:
                        raise UnicodeDecodeError
                except UnicodeDecodeError:
                    try:
                        char = chardet.detect(self.content)
                        if char:
                            text = self.content.decode(char['encoding'])
                        else:
                            raise UnicodeDecodeError
                    except UnicodeDecodeError:
                        try:
                            text = self.content.decode('utf-8')
                        except UnicodeDecodeError:
                            try:
                                text = self.content.decode("GBK")
                            except UnicodeDecodeError:
                                text = self.content.decode('utf-8', "ignore")
        else:
            try:
                text = self.content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    char = chardet.detect(self.content)
                    if char:
                        text = self.content.decode(char['encoding'])
                    else:
                        raise UnicodeDecodeError
                except UnicodeDecodeError:
                    try:
                        text = self.content.decode('gb2312')
                    except UnicodeDecodeError:
                        text = self.content.decode('utf-8', "ignore")
        return text

    @property
    def json(self):
        return js.loads(self.text, strict=False)

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
                logger.info("第%s次请求报错{%s:%s}，url：{%s}" % (retry_times, type(e).__name__, e, request['url']))
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
            async with session.get(URL(request['url'], encoded=request.get('url_encoded', False)),
                                   params=request.get('params', None), cookies=request.get('cookies', None),
                                   headers=request.get('headers', None), proxy=request.get('proxies', None),
                                   allow_redirects=request.get('allow_redirects', True),
                                   timeout=request.get('time_out', 180),
                                   proxy_auth=aiohttp.BasicAuth(fuclib.proxyUser, fuclib.proxyPass)) as res:
                text = await res.read()

        elif request['method'].upper() == 'POST':
            async with session.post(URL(request['url'], encoded=request.get('url_encoded', False)),
                                    data=request.get('data', None), json=request.get('json', None),
                                    cookies=request.get('cookies', None), headers=request.get('headers', None),
                                    proxy=request.get('proxies', None),
                                    allow_redirects=request.get('allow_redirects', True),
                                    timeout=request.get('time_out', 180),
                                    proxy_auth=aiohttp.BasicAuth(fuclib.proxyUser, fuclib.proxyPass)) as res:
                text = await res.read()
        else:
            raise MyException("{%s}请求方式未定义，请自定义添加！" % request['method'])

        if res:
            status_code = res.status
            charset = res.charset
            response = Response(request['url'], text, status_code, charset, request.get('cookies', None),
                                request['method'], request.get('headers', None), request.get('callback', "parse"),
                                request.get('proxies', None), request.get('meta', None), res)
            return response

    @staticmethod
    async def new_session(verify=False):
        connector = aiohttp.TCPConnector(ssl=verify)
        session = aiohttp.ClientSession(connector=connector, trust_env=True)
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
