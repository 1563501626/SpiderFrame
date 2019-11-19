
st = """
websiteId: 8676232ec118450ba0eff07aa583b54c
maxPage: 83
title: 
c_syh: 
tc_name: 
pagination_input: 2
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