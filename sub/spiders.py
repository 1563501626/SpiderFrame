# -*- coding: utf-8 -*-
import aiohttp
import chardet


class Response:
    def __init__(self, url, content=None, status_code=None, charset=None, cookies=None, method=None,
                 headers=None, callback="parse", proxies=None, meta=None):
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


class Request:

    async def quest(self, session, request):
        import asyncio  # TODO// +++++++++++++++++++++++++
        # with asyncio.Semaphore(200):

        await asyncio.sleep(2)
        res, text = await self.__getattribute__(request['method'].lower())(session, request)
        status_code = res.status
        charset = res.charset
        response = Response(request['url'], text, status_code, charset, request['cookies'], request['method'],
                            request['headers'], request['callback'], request['proxies'])
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
                               allow_redirects=request['allow_redirects']) as res:
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
        print(future.result())
        return future.result()
