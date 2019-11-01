# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import chardet


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
    def func(future):
        print(future.result())
        return future.result()


class Response:
    def __init__(self, url, content=None, status_code=None, charset=None, cookies=None, method=None,
                 headers=None, callback="parse", proxies=None, error=None, meta=None):
        self.url = url
        self.content = content
        self.status_code = status_code
        self.charset = charset
        self.cookies = cookies
        self.method = method
        self.headers = headers
        self.callback = callback
        self.proxies = proxies
        self.error = error
        self.meta = meta
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
                        text = content.decode(char)
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
