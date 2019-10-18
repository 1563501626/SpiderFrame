# -*- coding: utf-8 -*-
import aiohttp, asyncio
from DBUtils.PooledDB import PooledDB
import pymysql

async def quest(url, session=None):
    async with asyncio.Semaphore(200):
        if not session:
            session = aiohttp.ClientSession()
        res = await session.get(url)
        return session, await res.read()

# loop = asyncio.get_event_loop()
#
# tasks = []
# session = ''
# for i in ['http://www.baidu.com', 'http://www.baidu.com/s?wd=hello', 'http://www.baidu.com/s?wd=xixi']:
#     print('消费:', i)
#     s, _ = loop.run_until_complete(quest(i, session))
#     # print(_.decode())
#     if not session:
#         session = s
#     # tasks.append(session.get(i))
# # print(loop.run_until_complete(asyncio.wait(tasks)))
#
# loop.run_until_complete(session.close())
# loop.close()
# sql_pool = PooledDB(creator=pymysql, host='', user=self.sql_user, passwd=self.sql_pwd, db=self.sql_db, port=self.sql_port)
import pickle
from io import BytesIO
class A:
    a = 1

a = A()
x = pickle.dump(a)
print()