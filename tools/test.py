# # -*- coding: utf-8 -*-
# import sys
# import threading
# import traceback
#
#
# class ExceptErrorThread(threading.Thread):
#     def __init__(self, funcName, *args):
#         threading.Thread.__init__(self)
#         self.args = args
#         self.funcName = funcName
#         self.exitcode = 0
#         self.exception = None
#         self.exc_traceback = ''
#
#     def run(self):  # Overwrite run() method, put what you want the thread do here
#         try:
#             self._run()
#         except Exception as e:
#             self.exitcode = 1  # 如果线程异常退出，将该标志位设置为1，正常退出为0
#             self.exception = e
#             self.exc_traceback = ''.join(traceback.format_exception(*sys.exc_info()))  # 在改成员变量中记录异常信息
#
#     def _run(self):
#         try:
#             self.funcName(*(self.args))
#         except Exception as e:
#             raise e
#
# # import threading
# # import time
# # list = [0,0,0,0,0,0,0,0,0,0,0,0]
# # class myThread(threading.Thread):
# #     def __init__(self,threadId,name,counter):
# #         threading.Thread.__init__(self)
# #         self.threadId = threadId
# #         self.name = name
# #         self.counter = counter
# #     def run(self):
# #         print ("开始线程:",self.name)
# #         # 获得锁，成功获得锁定后返回 True
# #         # 可选的timeout参数不填时将一直阻塞直到获得锁定
# #         # 否则超时后将返回 False
# #         threadLock.acquire()
# #         print_time(self.name,self.counter,list.__len__())
# #         # 释放锁
# #         threadLock.release()
# #     def __del__(self):
# #         print (self.name,"线程结束！")
# # def print_time(threadName,delay,counter):
# #     while counter:
# #         time.sleep(delay)
# #         list[counter-1] += 1
# #         print ("[%s] %s 修改第 %d 个值，修改后值为:%d" % (time.ctime(time.time()),threadName,counter,list[counter-1]))
# #         counter -= 1
# # threadLock = threading.Lock()
# # threads = []
# # # 创建新线程
# # thread1 = myThread(1,"Thread-1",1)
# # thread2 = myThread(2,"Thread-2",2)
# # # 开启新线程
# # thread1.start()
# # thread2.start()
# # # 添加线程到线程列表
# # threads.append(thread1)
# # threads.append(thread2)
# # # 等待所有线程完成
# # for t in threads:
# #     t.join()
# # print ("主进程结束！", list)
#
# # import multiprocessing, time
# #
# # def runner():
# #     time.sleep(2)
# #     print(1)
# #
# # if __name__ == '__main__':
# #     p = multiprocessing.Process(target=runner)
# #     p.start()
# #     p.join()
# #     print('done')
# import requests
# import random
# import time
# import os
# import re
# from tqdm import tqdm
#
# user_agent = [
#     "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
#     "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
#     "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
#     "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
#     "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
#     "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
#     "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
#     "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
#     "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
#     "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
#     "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
#     "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
#     "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
#     "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
#     "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
#     "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
#     "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
#     "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
#     "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
#     "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
#     "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
#     "UCWEB7.0.2.37/28/999",
#     "NOKIA5700/ UCWEB7.0.2.37/28/999",
#     "Openwave/ UCWEB7.0.2.37/28/999",
#     "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
#     # iPhone 6：
#     "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
# ]
#
#
# def get_json(url, num):
#     headers = {
#         'User-Agent': random.choice(user_agent),
#         'Accept': 'application/json, text/plain, */*',
#         'Referer': 'http://vc.bilibili.com/p/eden/rank'
#     }
#     params = {
#         'page_size': 10,
#         'next_offset': str(num),
#         'tag': '今日热门',
#         'platform': 'pc'
#     }
#
#     try:
#         html = requests.get(url, params=params, headers=headers)
#         return html.json()
#
#     except:
#         print('request error')
#         pass
#
#
# def downloader(url, path):
#     size = 0
#     headers = {
#         'User-Agent': random.choice(user_agent)
#     }
#
#     r = requests.get(url, headers=headers, stream=True)  # stream属性必须带上
#     chunk_size = 1024  # 每次下载的数据大小
#     content_size = int(r.headers['content-length'])  # 总大小
#     if r.status_code == 200:
#         print('[文件大小]:%0.2f MB' % (content_size / chunk_size / 1024))  # 换算单位
#         if not os.path.exists(path):
#             start = time.time()  # 开始时间
#             with open(path, 'wb') as f:
#                 for data in tqdm(r.iter_content(chunk_size=chunk_size)):
#                     f.write(data)
#                     # size += len(data)  # 已下载的文件大小
#                     # print("已下载{:.2f}%".format(size/content_size*100))
#             stop = time.time()
#             print("下载本视频耗时{:.2f}s".format(stop - start))
#         else:
#             print("该视频之前已经完成下载！")
#
#
# def main():
#     count = 0
#     for i in range(10):
#         url = 'http://api.vc.bilibili.com/board/v1/ranking/top?'
#         num = i * 10 + 1
#         html = get_json(url, num)
#         infos = html['data']['items']
#         for info in infos:
#             count += 1
#             title = info['item']['description']  # 小视频的标题
#             # new_title = re.sub('[\t\|<>\?\*\\:/\[\]]', '', title)    # 去掉不符合文件命名规则的符号
#             video_url = info['item']['video_playurl']  # 小视频的下载链接
#             print(title)
#             try:
#                 downloader(video_url, path="{}.mp4".format(count))
#             except:
#                 print("下载失败！")
#                 pass
#
#
# if __name__ == '__main__':
#     main()


# def sort(res, first, last):
#     if first >= last:
#         return
#     head = res[first]
#     first_step = first
#     last_step = last
#     while first_step < last_step:
#         while res[last_step] >= head and first_step < last_step:
#             last_step -= 1
#         res[first_step] = res[last_step]
#         while res[first_step] < head and first_step < last_step:
#             first_step += 1
#         res[last_step] = res[first_step]
#     res[first_step] = head
#     sort(res, first, first_step-1)
#     sort(res, first_step+1, last)
#
#
# a = [4, 12, 7, 1, 8, 55, 10]
# sort(a, 0, len(a)-1)
# print(a)
# "iso-8859-1"
# import requests
# s = requests.session()
# headers = {
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
# }
# u1 = 'http://ghzyj.sh.gov.cn/2011/gcjsxx/xmxx/jsydsp/'
# res = s.get(u1, headers=headers)
# js1 = input('js1:')
# u2 = "http://ghzyj.sh.gov.cn" +js1
# res1 = s.get(u2)
# c2 = input('c2:')
# li2 = c2.split('=')
# c1 = {li2[0]:li2[1]}
# requests.utils.add_dict_to_cookiejar(s.cookies,c1)
# res22 = s.get(u1)
# for i in range(1, 10):
#     uu = "http://ghzyj.sh.gov.cn/2011/gcjsxx/xmxx/jsydsp/index_%s.html" % i
#     respp = s.get(uu)
#     print(respp.status_code)
#     if res.status_code != 200:
#         break
# print()

"iso-8859-1"
import requests
from spider import selector
import execjs
s = requests.session()
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}
u1 = 'http://ghzyj.sh.gov.cn/2011/gcjsxx/xmxx/jsydsp/'
res = s.get(u1, headers=headers)
ret = selector(res)
js1 = ret.xpath("//script[@charset='iso-8859-1']/@src").extract_first()
content = ret.xpath("//meta[@http-equiv='Content-Type']/following::meta[1]/@content").extract_first()
func1 = ret.xpath("string(//script[@charset='iso-8859-1']//following::script[1])").extract_first()
u2 = "http://ghzyj.sh.gov.cn" +js1
res1 = s.get(u2)
func2 = res1.content.decode("iso-8859-1")
with open(r"C:\Users\15635\Desktop\pdd\test.js", 'r', encoding='utf8') as f:
    js = f.read()
jsp = execjs.compile(js, cwd=r'C:\Users\15635\AppData\Roaming\npm\node_modules')
coo = jsp.call("ff1", content, func1, func2)

c2 = coo.split(';')[-1].strip()
li2 = c2.split('=')
c1 = {li2[0]:li2[1]}
requests.utils.add_dict_to_cookiejar(s.cookies,c1)
res22 = s.get(u1)
for i in range(1, 10):
    uu = "http://ghzyj.sh.gov.cn/2011/gcjsxx/xmxx/jsydsp/index_%s.html" % i
    respp = s.get(uu)
    print(respp.status_code)
    if respp.status_code != 200:
        break
print()
