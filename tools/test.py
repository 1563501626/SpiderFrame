# -*- coding: utf-8 -*-
# import aiohttp, asyncio
# from DBUtils.PooledDB import PooledDB
# import pymysql

# async def quest(url, session=None):
#     async with asyncio.Semaphore(200):
#         if not session:
#             session = aiohttp.ClientSession()
#         res = await session.get(url)
#         return session, await res.read()

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

# def a(**kwargs):
#     print(kwargs)
#     print(*kwargs)
#     print(**kwargs)
#
# def b(a=1, b=2, c=3):
#     print(a)
#
# b({'a': 1, 'b': 2, 'c': 3})

import requests
# url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
# headers = {
# 'accept':'*/*',
# 'accept-encoding':'gzip,deflate,br',
# 'accept-language':'zh-CN,zh;q=0.9',
# 'cache-control':'no-cache',
# 'content-length':'484',
# 'content-type':'application/x-www-form-urlencoded',
# 'cookie':'_zap=a91ce2ab-c004-4049-afd2-371d6945f47a; d_c0="ANCgBgK-9Q-PTu6NT3oHH9SSGL8H297ZVjs=|1566969518"; _xsrf=ys2mFPmZ809EuK1xPLDygr6HfBIiFwpl; l_n_c=1; n_c=1; q_c1=8ff69804f2284ee388f9434916fcd606|1569827177000|1569827177000; __utma=51854390.299791589.1569827179.1569827179.1569827179.1; __utmc=51854390; __utmz=51854390.1569827179.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.100--|2=registration_date=20190927=1^3=entry_date=20190927=1; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1572591453; tgw_l7_route=d9073c2db8fd446afafd830a80e5db8c; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1572600251; capsion_ticket="2|1:0|10:1572600252|14:capsion_ticket|44:MzNkYWZlMTk4ZDViNDljMjhjYTJhMDYwNjkwOWVkN2Y=|0fd11a50ceecd6bb75d9e66c3b51ffa1fdf3f571bf326dd2cd10127977d615c4"',
# 'origin':'https://www.zhihu.com',
# 'pragma':'no-cache',
# 'referer':'https://www.zhihu.com/signin?next=%2F',
# 'sec-fetch-mode':'cors',
# 'sec-fetch-site':'same-origin',
# 'user-agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/77.0.3865.120Safari/537.36',
# 'x-ab-param':'se_ltr_user=0;tsp_billboardhead=1;li_qa_new_cover=1;se_whitelist=0;li_search_answer=0;se_cardrank_2=0;se_ad_index=10;se_famous=1;tp_sft_v2=d;li_se_heat=1;top_hotcommerce=1;se_colorfultab=1;tp_qa_metacard=1;tsp_newchild=1;li_se_media_icon=0;se_webmajorob=0;se_time=0.5;se_hotsearch=1;se_auto_syn=0;se_time_threshold=0;tp_topic_head=0;pf_foltopic_usernum=50;zr_km_recall=default;zr_video_rank_nn=new_rank;zr_rel_search=base;zr_video_rank=new_rank;se_club_post=5;se_mobileweb=1;li_salt_hot=0;zr_ans_rec=gbrank;zr_intervene=0;zr_km_recall_num=close;se_zu_onebox=0;se_waterfall=0;se_use_zitem=0;li_purchase_test=0;li_pay_banner_type=0;soc_yxzl_zcfw=0;ug_follow_topic_1=2;ls_zvideo_like=0;top_quality=0;soc_bignew=1;se_ab=0;se_adxtest=1;ls_fmp4=0;li_hot_score_ab=0;se_expired_ob=0;se_ios_spb309=0;se_col_boost=0;se_topicfeed=0;se_cardrank_1=0;top_universalebook=1;top_vipconsume=1;qap_ques_invite=0;zr_cold_start=0;tsp_hotctr=1;pf_noti_entry_num=0;se_movietab=1;tp_club_qa_pic=0;se_mclick=0;se_pro=0;se_webrs=1;se_featured=1;li_qa_btn_text=0;se_search_feed=N;top_v_album=1;ug_fw_answ_aut_1=0;ug_newtag=0;zr_recall_heatscore=false;se_dnn_unbias=1;top_native_answer=1;soc_zcfw_broadcast=0;se_college_cm=0;se_lottery=0;soc_notification=0;li_se_section=0;se_billboardsearch=0;se_ltr_cp_new=0;ug_follow_answerer=0;zr_slot_cold_start=aver;zr_km_feed_prerank=new;se_ctr_user=0;se_cardrank_4=1;soc_special=0;zr_answer_rec_cp=open;se_spb309=0;zr_infinity_member=close;se_perf=0;se_cardrank_3=0;tp_meta_card=0;top_new_feed=5;soc_zcfw_badcase=0;zr_km_feed_nlp=old;zr_km_special=close;se_payconsult=0;tp_header_style=1;soc_update=1;soc_stickypush=0;soc_zcfw_shipinshiti=0;zr_art_rec=base;zr_km_prerank=new;qap_payc_invite=0;zw_sameq_sorce=999;zr_article_new=close;zr_prerank_heatscore=false;zr_filter=false;se_entity_model=0;li_video_section=0;se_hot_timebox=0;pf_newguide_vertical=0;ug_goodcomment_0=1;se_aa_base=0;se_zu_recommend=0;se_p_slideshow=0;ug_zero_follow_0=0;li_se_kv=0;se_ctx=0;zr_rec_answer_cp=close;se_ctr_topic=0;se_wannasearch=0;ug_zero_follow=0;ls_videoad=2;li_book_button=0;zr_video_recall=current_recall;se_mclick1=0;se_ctr_pyc=0;li_qa_cover=old;se_new_topic=0;se_sug=0;li_se_paid_answer=0;zr_km_answer=open_cvr;zr_new_commodity=0;se_webtimebox=0;se_dnn_mt=0;se_hotmore=0;se_bst=0;se_backsearch=0;top_ydyq=X;ls_zvideo_license=0;top_root=0;soc_bigone=0;zr_paid_answer_mix=mixed_20;tp_sft=a;zr_km_category=close;zr_slotpaidexp=1;zr_item_nn_recall=close;se_sepciality=0;tsp_vote=1;li_android_vip=0;li_se_album_card=0;zr_km_topic_zann=old;se_likebutton=0;se_websearch=3;tp_m_intro_re_topic=1;tsp_billboardsheep2=1;ug_follow_answerer_0=0;sem_up_growth=in_app;ls_zvideo_trans=0;zw_payc_qaedit=0;zr_km_item_cf=close;zr_km_slot_style=event_card;zr_man_intervene=0;se_subtext=0;pf_fuceng=1;li_album_liutongab=0;ls_new_upload=0;se_amovietab=1;tp_club_qa=1;tp_qa_toast=1;soc_zuichangfangwen=0;li_vip_no_ad_mon=0;se_ltr_dnn_cp=0;zr_search_xgb=1;top_ebook=0;pf_creator_card=1;zr_test_aa1=0;se_preset_tech=0;se_topiclabel=1;se_agency=0;tp_sticky_android=2;tp_qa_metacard_top=top;tsp_childbillboard=1;top_test_4_liguangyi=1;se_go_ztext=0;se_college=default;li_se_vertical=0;zr_km_item_prerank=old;zr_km_style=base;se_site_onebox=0;li_se_xgb=0;li_tjys_ec_ab=0',
# 'x-requested-with':'fetch',
# 'x-xsrftoken':'ys2mFPmZ809EuK1xPLDygr6HfBIiFwpl',
# 'x-zse-83':'3_2.0',
# }
# resp = requests.get('data:image/jpg;base64,R0lGODdhlgA8AIcAAP7+/gAAAOjo6CcnJ9fX18jIyBYWFmZmZkZGRoeHh/Ly8ldXVzU1NXZ2dqen%0Ap5aWlrm5ubi4uDc3N6WlpSsrK8HBwZ6engAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAAlgA8AEAI/wABCBxI%0AsKDBgwgTKlzIsKHDhxAjSpxIsaLFixgzKiRQQIAABQBCihQZoOQAAgBSqlzJUgCCAAEkBJiJQACA%0AmzhvCngwIIDPAAYgBBgagACAo0iTKl3KtKnTp1CVTghAleoDAFizasX6IIDXAwACiA0QAYDZs2jT%0A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%0AKdSoUqdSrWr16tSAADs=', headers={'user-agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/77.0.3865.120Safari/537.36',})
# session = requests.session()
# data = "aR79k4U0cT2tXqYq8LPG6vHmxq2pkLnmtbSBDgg9kLtxgeSmhbfGiqX1jbfVoG398LF0gQN0cT2tuqYq8LkMQbwGivwOgUxGw9e0g4e8kCV92vgBzh3qk4R92LkYFhVGwqoVJbCGST2tECx9BLkBEJXmST2tXqYhZUS8eDC8FBtxgLO1RCp1QHuqc7FpXqYhyhomogcMUuppkLk0s_2qeQuqSXYxr8tyihYqk4R92LkYJwNm8CSMcrU0gTtYSLY00wNBoTUqgwFpSTx0fTY8gvUqrH2pQXY8zhFqQQuqHw2pk8t9BLfBkvwGUbOYDq3q8Ln8gcgZcUS_iD3ZpvS8Xg9hgqxOcvSMMTYhr7uy28txr7Yq8MYqr6S0gRo9U9oMzcO1erU0g_xO-GoMBwxMXg9hguoLevwGXwNM3rU0gRtxguFqm0YBrAHqgg2f2Txy0qtq6A98S8Yfo8OBhq28Xg9hHgOGebOBtrS8"
# res = session.post(url, headers=headers, data=data)
# print()
#
# import base64
# r=  base64.b64decode("AxjgB5MAnACoAJwBpAAAABAAIAKcAqgAMAq0AzRJZAZwUpwCqACQACACGAKcBKAAIAOcBagAIAQYAjAUGgKcBqFAuAc5hTSHZAZwqrAIGgA0QJEAJAAYAzAUGgOcCaFANRQ0R2QGcOKwChoANECRACQAsAuQABgDnAmgAJwMgAGcDYwFEAAzBmAGcSqwDhoANECRACQAGAKcD6AAGgKcEKFANEcYApwRoAAxB2AGcXKwEhoANECRACQAGAKcE6AAGgKcFKFANEdkBnGqsBUaADRAkQAkABgCnBagAGAGcdKwFxoANECRACQAGAKcGKAAYAZx+rAZGgA0QJEAJAAYA5waoABgBnIisBsaADRAkQAkABgCnBygABoCnB2hQDRHZAZyWrAeGgA0QJEAJAAYBJwfoAAwFGAGcoawIBoANECRACQAGAOQALAJkAAYBJwfgAlsBnK+sCEaADRAkQAkABgDkACwGpAAGAScH4AJbAZy9rAiGgA0QJEAJACwI5AAGAScH6AAkACcJKgAnCWgAJwmoACcJ4AFnA2MBRAAMw5gBnNasCgaADRAkQAkABgBEio0R5EAJAGwKSAFGACcKqAAEgM0RCQGGAYSATRFZAZzshgAtCs0QCQAGAYSAjRFZAZz1hgAtCw0QCQAEAAgB7AtIAgYAJwqoAASATRBJAkYCRIANEZkBnYqEAgaBxQBOYAoBxQEOYQ0giQKGAmQABgAnC6ABRgBGgo0UhD/MQ8zECALEAgaBxQBOYAoBxQEOYQ0gpEAJAoYARoKNFIQ/zEPkAAgChgLGgkUATmBkgAaAJwuhAUaCjdQFAg5kTSTJAsQCBoHFAE5gCgHFAQ5hDSCkQAkChgBGgo0UhD/MQ+QACAKGAsaCRQCOYGSABoAnC6EBRoKN1AUEDmRNJMkCxgFGgsUPzmPkgAaCJwvhAU0wCQFGAUaCxQGOZISPzZPkQAaCJwvhAU0wCQFGAUaCxQMOZISPzZPkQAaCJwvhAU0wCQFGAUaCxQSOZISPzZPkQAaCJwvhAU0wCQFGAkSAzRBJAlz/B4FUAAAAwUYIAAIBSITFQkTERwABi0GHxITAAAJLwMSGRsXHxMZAAk0Fw8HFh4NAwUABhU1EBceDwAENBcUEAAGNBkTGRcBAAFKAAkvHg4PKz4aEwIAAUsACDIVHB0QEQ4YAAsuAzs7AAoPKToKDgAHMx8SGQUvMQABSAALORoVGCQgERcCAxoACAU3ABEXAgMaAAsFGDcAERcCAxoUCgABSQAGOA8LGBsPAAYYLwsYGw8AAU4ABD8QHAUAAU8ABSkbCQ4BAAFMAAktCh8eDgMHCw8AAU0ADT4TGjQsGQMaFA0FHhkAFz4TGjQsGQMaFA0FHhk1NBkCHgUbGBEPAAFCABg9GgkjIAEmOgUHDQ8eFSU5DggJAwEcAwUAAUMAAUAAAUEADQEtFw0FBwtdWxQTGSAACBwrAxUPBR4ZAAkqGgUDAwMVEQ0ACC4DJD8eAx8RAAQ5GhUYAAFGAAAABjYRExELBAACWhgAAVoAQAg/PTw0NxcQPCQ5C3JZEBs9fkcnDRcUAXZia0Q4EhQgXHojMBY3MWVCNT0uDhMXcGQ7AUFPHigkQUwQFkhaAkEACjkTEQspNBMZPC0ABjkTEQsrLQ==").decode('utf8', 'ignore')
# print(r)

# href = "http://yangkeduo.com/search_catgoods.html?opt_id=9503&opt1_id=999998&opt2_id=999999&opt_g=1&opt_type=3&opt_name=%E5%8D%AB%E8%A1%A3&_x_link_id=08572bef-6c59-495a-b580-e88d3a4139fb&refer_page_name=search&refer_page_id=10031_1573736442111_4Cvy1RF2Rj&refer_page_sn=10031"
# headers = {'AccessToken':'5LDVDFD6PLIGP7HRLVFBH6K2CV4ZPSMD7PIJUDHJSFTSO5FHOV3Q1107115',
# 'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
# 'Origin':'http://yangkeduo.com',
# 'Referer':'http://yangkeduo.com/search_catgoods.html?opt_id=9503&opt1_id=999998&opt2_id=999999&opt_g=1&opt_type=3&opt_name=%E5%8D%AB%E8%A1%A3&_x_link_id=08572bef-6c59-495a-b580-e88d3a4139fb&refer_page_name=search&refer_page_id=10031_1573736442111_4Cvy1RF2Rj&refer_page_sn=10031',
# 'User-Agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/76.0.3809.100Safari/537.36',
# 'VerifyAuthToken':'kOLkOBEfTnA121StiaCfqQ',
# }
# content = "0anAfxnUvOhYq9mavj8DgCPopH_HZe_uzfnLQZ_VsBVIV_TOZBYvvIWSZwjG-OcpDlOLmlgAlgLrBdV3u0gP8LoqiWhmJJHcTX9C0R2zLCnPl5YTlWvno5jzMSThBZbV94yR962ibkRT2WAymY-RdJQGHGWmvj7Loa5Ji7wTH-DTCitqsCKIoKZnR01145U_SRIGQyTFGzDxf60XAY8eLPpLDfDkpbtKbvcn4PLyKO_57E2nRmxnut-7GXRkcXpDzKIE3tnkuNucj-_GNS4D6QGNsdJs9s8VHqV8O0MnVJ1jbDdEJT3SuihvtC1ORTZNv0brnKRaYYpoeC_F84GzFToeVf470kb8e4GpiDsNkXeCBmo5DcCNLPGNIi09bZSy3esl7zggXTYHm8gmnW4HgUJaoLEVL6W2dr2A9lqsGgTtxU08xA-6pD7dSV9UZE7lCf5towQJ0GSb9jj7SXNcB3ib0-JVDz1qSOOU1kAo7zX2FufGScLsWS3TopIi2Cy9rBlYv1oTqTcxywutWrY1TylGeYtn05NX5HRlYfKHF0SHoSza_Bkaszwtmlxukap2qQuHu4Fs8Kvr5ms5c2-neZ7YKJhS8ziuQxmqbeqaJY4ApGQe-PxhkW7FieeoGkqireNdRi8ioNdSI6o"
# url = "http://apiv3.yangkeduo.com/api/search/opt/9503/groups?gid=&source=search&opt_type=3&flip=40;3;0;20;781b12ce-ce1e-460b-b157-1baff9f903c1&offset=40&count=20&list_id=OSO6zSH0VP&sort=default&filter=&anti_content=%s&pdduid=2594367865969"%content
# # url = "http://apiv3.yangkeduo.com/api/search/opt/9503/groups?gid=&source=search&opt_type=3&flip=40;3;0;20;781b12ce-ce1e-460b-b157-1baff9f903c1&offset=40&count=20&list_id=OSO6zSH0VP&sort=default&filter=&anti_content=0anAfxnUXycYY9dVzRBY4t2a2S2YZ0VtfdkArDjituvVgt_sVwkd4ZYTUZzLwM6pVqD_vqxraEr9R9AG6UwuIo0p2fdHzTj8bxImJ3cDCY9YBuSS6zgJfg47irVP2PQgWxdlstCNUhxSoGturU_L1nsfEmQgta9C_rRTggrIny4JRV8dF7FUk3hCMoJshx3YtfZSHNsXPH_Qo11Ev6oceedUiaedveixFHAPjeuRcFzDf3LUmknN0D_6LDSFOz1styOoXi0ZzZKQkk37D7N7ljbkKc1DDQcGRYHqmAD9cPxaoVs8GT5b5dO5o7nUG-Utvx7-Jssp_rl3qXwZbFW2Ula1NaOiiNEnFs4plKpbKZlkvczT_MyIm3MswjmBPQw5wMCGHS_A_V7Cpj9fxCv5x84GBKbOcXwJKVBmyWZlPo_xJvNFPTt89sJZZEeO-PZlPR4U2KcqP56DphZy42cLnUx6mnOnPy1cmT3UnV6x3U48ReCC_SaQxhzkeEslOXPDFx-l_rzm8aiC_Mwx0Bz9NH3aUhDlH0OHHqgKT5LkkdqYNsXBqW3GxLl7V8ZG2YGW41Zm7B9lr-H-95uHpzZ-_Lan6UsR0kPCyM3nok6k0vh7fvrFf6ANP1N43RP-y6ciAWu9kU3IqHM8TrhlpMOrR4N-dI8uW7WL5i7qGEv&pdduid=2594367865969"
# res = requests.get(url, headers=headers)
# print(res.text)
# print()


import aiohttp
import asyncio
import sys
import threading




class Retry:
    def __init__(self, max_times):
        self.func = None
        self.max_times = max_times
        self.retry_times = 0

    def run(self, aa, b):
        while self.max_times:
            try:
                return self.func(aa, b)
            except asyncio.TimeoutError:
                self.retry_times += 1
                self.max_times -= 1
                print("第%s次请求超时" % self.retry_times)
                # await self.run()

    def __call__(self, func):
        self.func = func
        return self.run


def retry(max_times):
    def outer(func):
        def inner(session, ret):
            nonlocal max_times
            retry_times = 0
            while max_times:
                try:
                    return func(session, ret)
                except asyncio.TimeoutError:
                    retry_times += 1
                    max_times -= 1
                    print("第%s次请求超时" % retry_times)
        return inner
    return outer

# @Retry(max_times=3)
async def a():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=True)) as s:
        print('qingiuq ')
        async with s.get('http://www.gchjgv.com', timeout=1) as res:
            text = await res.read()
    return text

@Retry(max_times=3)  #go = Retry(max_times=3)(go)(...)
def go(aa, b):
    loop = asyncio.get_event_loop()
    ret = loop.run_until_complete(a())

import traceback
# try:
#     go(1,2)
#     print('done')
# except:
#     traceback.print_exc()
# ret = a()
# print(ret)




import functools
import logging
import time
import pika

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class ExampleConsumer(object):

    EXCHANGE = 'message'
    EXCHANGE_TYPE = 'topic'
    QUEUE = 'text'
    ROUTING_KEY = 'example.text'

    def __init__(self, amqp_url):

        self.should_reconnect = False
        self.was_consuming = False

        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._url = amqp_url
        self._consuming = False
        # In production, experiment with higher prefetch values
        # for higher consumer throughput
        self._prefetch_count = 1

    def connect(self):

        LOGGER.info('Connecting to %s', self._url)
        return pika.SelectConnection(
            parameters=pika.URLParameters(self._url),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed)

    def close_connection(self):
        self._consuming = False
        if self._connection.is_closing or self._connection.is_closed:
            LOGGER.info('Connection is closing or already closed')
        else:
            LOGGER.info('Closing connection')
            self._connection.close()

    def on_connection_open(self, _unused_connection):

        LOGGER.info('Connection opened')
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err):

        LOGGER.error('Connection open failed: %s', err)
        self.reconnect()

    def on_connection_closed(self, _unused_connection, reason):

        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            LOGGER.warning('Connection closed, reconnect necessary: %s', reason)
            self.reconnect()

    def reconnect(self):

        self.should_reconnect = True
        self.stop()

    def open_channel(self):

        LOGGER.info('Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):

        LOGGER.info('Channel opened')
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self.EXCHANGE)

    def add_on_channel_close_callback(self):

        LOGGER.info('Adding channel close callback')
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reason):

        LOGGER.warning('Channel %i was closed: %s', channel, reason)
        self.close_connection()

    def setup_exchange(self, exchange_name):

        LOGGER.info('Declaring exchange: %s', exchange_name)
        # Note: using functools.partial is not required, it is demonstrating
        # how arbitrary data can be passed to the callback when it is called
        cb = functools.partial(
            self.on_exchange_declareok, userdata=exchange_name)
        self._channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=self.EXCHANGE_TYPE,
            callback=cb)

    def on_exchange_declareok(self, _unused_frame, userdata):

        LOGGER.info('Exchange declared: %s', userdata)
        self.setup_queue(self.QUEUE)

    def setup_queue(self, queue_name):

        LOGGER.info('Declaring queue %s', queue_name)
        cb = functools.partial(self.on_queue_declareok, userdata=queue_name)
        self._channel.queue_declare(queue=queue_name, callback=cb)

    def on_queue_declareok(self, _unused_frame, userdata):

        queue_name = userdata
        LOGGER.info('Binding %s to %s with %s', self.EXCHANGE, queue_name,
                    self.ROUTING_KEY)
        cb = functools.partial(self.on_bindok, userdata=queue_name)
        self._channel.queue_bind(
            queue_name,
            self.EXCHANGE,
            routing_key=self.ROUTING_KEY,
            callback=cb)

    def on_bindok(self, _unused_frame, userdata):

        LOGGER.info('Queue bound: %s', userdata)
        self.set_qos()

    def set_qos(self):

        self._channel.basic_qos(
            prefetch_count=self._prefetch_count, callback=self.on_basic_qos_ok)

    def on_basic_qos_ok(self, _unused_frame):

        LOGGER.info('QOS set to: %d', self._prefetch_count)
        self.start_consuming()

    def start_consuming(self):

        LOGGER.info('Issuing consumer related RPC commands')
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(
            self.QUEUE, self.on_message)
        self.was_consuming = True
        self._consuming = True

    def add_on_cancel_callback(self):

        LOGGER.info('Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):

        LOGGER.info('Consumer was cancelled remotely, shutting down: %r',
                    method_frame)
        if self._channel:
            self._channel.close()

    def on_message(self, _unused_channel, basic_deliver, properties, body):

        LOGGER.info('Received message # %s from %s: %s',
                    basic_deliver.delivery_tag, properties.app_id, body)
        self.acknowledge_message(basic_deliver.delivery_tag)

    def acknowledge_message(self, delivery_tag):

        LOGGER.info('Acknowledging message %s', delivery_tag)
        self._channel.basic_ack(delivery_tag)

    def stop_consuming(self):

        if self._channel:
            LOGGER.info('Sending a Basic.Cancel RPC command to RabbitMQ')
            cb = functools.partial(
                self.on_cancelok, userdata=self._consumer_tag)
            self._channel.basic_cancel(self._consumer_tag, cb)

    def on_cancelok(self, _unused_frame, userdata):

        self._consuming = False
        LOGGER.info(
            'RabbitMQ acknowledged the cancellation of the consumer: %s',
            userdata)
        self.close_channel()

    def close_channel(self):

        LOGGER.info('Closing the channel')
        self._channel.close()

    def run(self):

        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):

        if not self._closing:
            self._closing = True
            LOGGER.info('Stopping')
            if self._consuming:
                self.stop_consuming()
                self._connection.ioloop.start()
            else:
                self._connection.ioloop.stop()
            LOGGER.info('Stopped')


class ReconnectingExampleConsumer(object):

    def __init__(self, amqp_url):
        self._reconnect_delay = 0
        self._amqp_url = amqp_url
        self._consumer = ExampleConsumer(self._amqp_url)

    def run(self):
        while True:
            try:
                self._consumer.run()
            except KeyboardInterrupt:
                self._consumer.stop()
                break
            self._maybe_reconnect()

    def _maybe_reconnect(self):
        if self._consumer.should_reconnect:
            self._consumer.stop()
            reconnect_delay = self._get_reconnect_delay()
            LOGGER.info('Reconnecting after %d seconds', reconnect_delay)
            time.sleep(reconnect_delay)
            self._consumer = ExampleConsumer(self._amqp_url)

    def _get_reconnect_delay(self):
        if self._consumer.was_consuming:
            self._reconnect_delay = 0
        else:
            self._reconnect_delay += 1
        if self._reconnect_delay > 30:
            self._reconnect_delay = 30
        return self._reconnect_delay


def main():
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    amqp_url = 'amqp://guest:guest@localhost:5672/%2F'
    consumer = ReconnectingExampleConsumer(amqp_url)
    consumer.run()


if __name__ == '__main__':
    main()