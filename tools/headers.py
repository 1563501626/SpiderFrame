
st = """
AccessToken: 5LDVDFD6PLIGP7HRLVFBH6K2CV4ZPSMD7PIJUDHJSFTSO5FHOV3Q1107115
Content-Type: application/x-www-form-urlencoded;charset=UTF-8
Origin: http://yangkeduo.com
Referer: http://yangkeduo.com/search_catgoods.html?opt_id=9503&opt1_id=999998&opt2_id=999999&opt_g=1&opt_type=3&opt_name=%E5%8D%AB%E8%A1%A3&_x_link_id=08572bef-6c59-495a-b580-e88d3a4139fb&refer_page_name=search&refer_page_id=10031_1573736442111_4Cvy1RF2Rj&refer_page_sn=10031
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36
VerifyAuthToken: kOLkOBEfTnA121StiaCfqQ
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36
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