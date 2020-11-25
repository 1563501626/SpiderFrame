import aiohttp
import asyncio
import threading
from aiohttp_requests import requests
import fuclib
from sub.spiders import Request
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
proxy_auth = aiohttp.BasicAuth(fuclib.proxyUser, fuclib.proxyPass)
async def aa(url,  headers='', data=None,p=None, method='POST'):
    con = aiohttp.TCPConnector(verify_ssl=False)
    async with aiohttp.ClientSession(connector=con, trust_env=True) as sess:
    #     if method.upper() == 'GET':
    #         async with sess.get(url, headers=headers, proxy=p, proxy_auth=proxy_auth) as res:
    #             content = await res.read()
    #     else:
    #         async with sess.post(url, headers=headers, data=data, proxy=p, proxy_auth=proxy_auth) as res:
    #             content = await res.read()
    # return content
        return await Request.quest(sess, {'method':'post', 'url':url,"headers":headers,'data':data, "proxies":p}, 3)
        # return await Request.quest(sess, {'method':'get', 'url':url,"headers":{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'},'data':data, "proxies":p}, 3)


def forever(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


if __name__ == '__main__':

    proxy_res = fuclib.getIP()
    # proxies = "http://" +fuclib.proxyUser+":"+fuclib.proxyPass+"@"+proxy_res['proxy'].replace("http://", "")
    # proxies = "http://123.207.11.119:1080"
    proxies = proxy_res['proxy']
    print(proxies)
    headers = {'Host': 'www.lubanlebiao.com',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
               'Accept': 'text/html, */*; q=0.01',
               'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
               'Accept-Encoding': 'gzip, deflate, br', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://www.lubanlebiao.com',
               'Referer': 'https://www.lubanlebiao.com/zz', "Proxy-Authorization": fuclib.proxyAuth}
    data = 'qyIds=632675&sf=10000&display[]={"dlId":"100000007001","xlId":"100000007001001","zyId":"100000007001001001","djId":"10000","fs":"0","zcd":"","provinceCode":"0","entrySign":"-1","lxId":"100000007"}&provinceCode=0&provinceSimpleName=&xmForm=&keyword=&page=1'
    url = 'https://www.lubanlebiao.com/ajax/zz'
    # url = 'https://api.ipify.org/?format=jsonp&callback=jQuery1102043952430295619105_1599099251399&_=1599099251400'
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'}
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=forever, args=(loop,))
    t.setDaemon(True)
    t.start()
    ret = asyncio.run_coroutine_threadsafe(aa(url, headers, data, proxies, 'post'), loop)
    print(ret.result())

# loop = asyncio.get_event_loop()
# loop.run_until_complete(apost())
# loop.close()
