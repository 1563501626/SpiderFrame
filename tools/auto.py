import os, time, multiprocessing, datetime, requests, json, re
from manager import run

x = "hj_taxcase"
sessionid = 'sessionid=ft2obmh2w8kpvqoq6xslgixjwd8rgs5m'
host = 'locallhost'


def runned(script):
    with open("_spider.cfg", 'w') as f:
        f.write("[spider/%s/%s]\nfunction = w\nasync_number = 1"%(x,script))
        f.flush()
        f.close()
    with open('../spider/%s/%s' % (x, script), 'r', encoding='utf8') as f:
        data = f.read()
        if 'self.insql' not in data:
            return
    run.start()


def myrun():
    headers = {
        'Cookie': sessionid,
        'Host': host,
        'Referer': 'http://%s/spider/basic.html' % host,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = requests.get("http://%s/data/" % host, headers=headers)
    datas = json.loads(data.text)['data'][:100]
    fsw_ls = []
    for i in datas:
        if i['path_name'].startswith(x):
            fsw_ls.append(i)
    for j in fsw_ls:
        # if j == 'fgz___pycache__':
        #     continue
        print(j)
        data = {
            'path_name': j["path_name"],
            'comment': j["comment"],
            'running': '',
            'updated': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'common_db_ip': j["common_db_ip"],
            'common_db': j["common_db"],
            'common_table': j["common_table"],
            'rabbitmq_ip': j["rabbitmq_ip"],
            'auto_update': '1',
            'update_freq': '24',
            'wash': '',
            'scz_wh216': 'on',
            'xfz_wh216': 'on',
        }
        ret = requests.post("http://%s/update/spider_basic_info/by_path_name/" % host, headers=headers,
                            data=data)
        print(1)


def begin():
    flie_ls = os.listdir("../spider/%s" % x)
    print(flie_ls)
    po = multiprocessing.Pool(1)
    for i in range(0, len(flie_ls)):
        if flie_ls[i] in ["__init__.py", "table.py", '__pycache__', 'read_doc_table.py', 'ztjzx_zhaob.py', 'ztjzx_zhongb.py', '1.py', '1.txt']:
            continue
        res = po.apply_async(runned, (flie_ls[i],))
        time.sleep(1)
    po.close()
    po.join()

def searchs(ret):
    url = "http://%s/es_select/basic/" % host
    headers = {
        'Cookie': sessionid,
        'Host': host,
        'Referer': 'http://%s/spider/basic.html' % host,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    f = open('a.txt', 'a', encoding='utf8')
    for i in ret:
        data = {'keyword':i}
        print(data)
        resp = requests.post(url, data=data, headers=headers).content.decode('unicode-escape')
        time.sleep(1)
        f.write(resp+'\n')
    f.close()

headers = {
        'Cookie': sessionid,
        'Host': host,
        'Referer': 'http://%s/spider/basic.html' % host,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

def modify(res):
    content = res['hits']['hits'][0]['_source']
    path_name = content['path_name']
    publish = content['publish']
    comsume = content['comsume']
    if 'ucloud216' not in publish and 'ucloud216' not in comsume:
        data = {'path_name':path_name}
        resp = requests.post('http://%s/select/by_path_name/' % host, data=data, headers=headers)
        j = json.loads(resp.content.decode('unicode-escape'))
        data = {
            'path_name': j["path_name"],
            'comment': j["comment"],
            'running': '',
            'updated': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'common_db_ip': j["common_db_ip"],
            'common_db': j["common_db"],
            'common_table': j["common_table"],
            'rabbitmq_ip': j["rabbitmq_ip"],
            'auto_update': '1',
            'update_freq': '24',
            'wash': '',
            'scz_wh216': 'on',
            'xfz_wh216': 'on',
        }
        ret = requests.post("http://%s/update/spider_basic_info/by_path_name/" % host, headers=headers,
                            data=data)
        if ret.status_code != 200:
            with open('b.txt', 'a', encoding='utf8') as f:
                f.write(path_name+'\n')


# **********************************************************************************************************************

import config
from importlib import import_module
import multiprocessing


mr = 'manager.run'
base = ['zcx']


def runn(paramslist):

    c = import_module(mr)
    c.start()


def get_path():
    headers = {'authorization': 'Basic d2FuZGVyOkVsZW1lbnRzMTIz',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}
    url = 'http://'+host+':15672/api/queues?page=1&page_size=100&name=%5Ezcx&use_regex=true&pagination=true'
    resp = requests.get(url, headers=headers)
    ret = json.loads(resp.content.decode())
    path_name = ret['items']
    result = list(map(lambda x:  x['name'] if x['messages_ready'] else '', path_name))
    return result


def aa():
    ret = get_path()
    for i in ret:
        if not i:
            continue
        multi_open = 0
        process_sum = 0
        async_number = 1
        for j in base:
            if j in i:
                path = j
                name = i.split(j)[-1][1:]
                break
        paramslist = [path, name, 'w', multi_open, process_sum, True, async_number]
        p = multiprocessing.Process(target=runn, args=(paramslist, ))
        p.start()
        p.join()


if __name__ == '__main__':
    # aa()
    pass



