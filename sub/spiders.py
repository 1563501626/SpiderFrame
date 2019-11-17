# -*- coding: utf-8 -*-
import asyncio
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


class Retry:
    def __init__(self, max_times):
        self.func = None
        self.max_times = max_times
        self.retry_times = 0

    async def run(self, req, session, ret):
        while self.max_times:
            try:
                response = await self.func(req, session, ret)
                if response and response.status_code not in ret['allow_code']:
                    self.retry_times += 1
                    self.max_times -= 1
                    print("第%s次请求失败,错误码:%s, url:%s" % (self.retry_times, response.status_code, ret['url']))
                else:
                    return response
            except asyncio.TimeoutError:
                self.retry_times += 1
                self.max_times -= 1
                print("第%s次请求超时, url:%s" % (self.retry_times, ret['url']))
            except Exception as e:
                self.retry_times += 1
                self.max_times -= 1
                print("第%s次请求报错, url:%s" % (self.retry_times, ret['url']))

    def __call__(self, func):
        self.func = func
        return self.run


class Request:
    async def quest(self, session, request, max_times):

        # @Retry(max_times=max_times)
        # async def start_quest(self, session, request):
        #     res, text = await self.__getattribute__(request['method'].lower())(session, request)
        #     status_code = res.status
        #     charset = res.charset
        #     response = Response(request['url'], text, status_code, charset, request['cookies'], request['method'],
        #                         request['headers'], request['callback'], request['proxies'])
        #     return response
        #
        # return await start_quest(self, session, request)
        for i in range(3):
            try:
                res, text = await self.__getattribute__(request['method'].lower())(session, request)
                status_code = res.status
                charset = res.charset
                response = Response(request['url'], text, status_code, charset, request['cookies'], request['method'],
                                    request['headers'], request['callback'], request['proxies'])
                return response
            except Exception:
                print("第%s次请求"%i)
                continue
        else:
            return None

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
                                allow_redirects=request['allow_redirects'], timeout=request['time_out']) as res:
            text = await res.read()
            return res, text

    @staticmethod
    async def exit(session):
        await session.close()

    # @staticmethod
    # def func(future):
    #     print(future.result())
    #     return future.result()
