# -*- coding: utf-8 -*-
from parsel import Selector


def selector(res, encode=None):
    if hasattr(res, 'ok'):
        if encode:
            resp = Selector(res.content.decode(encode))
        else:
            apparent_encoding = res.apparent_encoding
            if '2312' in apparent_encoding or 'dows' in apparent_encoding or '8859' in apparent_encoding:
                apparent_encoding = 'gbk'
            try:
                resp = Selector(res.content.decode(apparent_encoding))
            except:
                resp = Selector(res.content.decode(apparent_encoding, 'ignore'))
    else:
        if isinstance(res, str):
            resp = Selector(res)
        else:
            resp = Selector(res.text)
    return resp