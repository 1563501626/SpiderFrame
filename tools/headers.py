
st = """
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
referer: https://www.zhipin.com/c101200100/?page=4&ka=page-4
sec-fetch-mode: navigate
sec-fetch-site: same-origin
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36
"""

content_li = st.split('\n')
for i in content_li:
    if not i:
        continue
    head = ''
    if i.startswith(':'):
        i = i[1:]
        head = ':'
    i = i.replace(' ', '').replace(':', "':'", 1)
    print("'"+head+i+"',")