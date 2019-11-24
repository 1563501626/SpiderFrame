# -*- coding: utf-8 -*-

# rabbit_mq
mq_host = 'localhost'
mq_port = 5672
mq_user = 'guest'
mq_pwd = 'guest'
get_queue_info_delay = 60  # 访问队列信息api间隔（单位：s）

# mysql
sql_host = 'localhost'
sql_port = 3306
sql_user = 'root'
sql_pwd = '123456'
sql_db = 'frametest'

# 爬虫配置信息
spider_host = 'localhost'
spider_port = 3306
spider_user = 'root'
spider_pwd = '123456'
spider_db = 'spider_info'
spider_table = 'spider_update'  # 自动更新配置

# 自动更新配置
auto_step = 50  # 每一次处理多少个脚本
