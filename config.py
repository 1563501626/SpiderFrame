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
sql_db = 'spider_info'

# 爬虫配置信息
spider_host = 'localhost'
spider_port = 3306
spider_user = 'root'
spider_pwd = '123456'
spider_db = 'spider_info'
spider_table = 'spider_update'  # 自动更新配置


# 自动更新配置
auto_step = 50  # 每一次处理多少个脚本

"""
spider_table必须字段：
Create Table: CREATE TABLE `spider_update` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `path` varchar(100) NOT NULL,
  `queue_name` varchar(20) DEFAULT NULL,
  `async_num` int(11) DEFAULT '1',
  `auto_frequency` float(6,3) DEFAULT '-1.000',
  `update_machine` text NOT NULL,
  `cookie_update` tinyint(1) DEFAULT '0',
  `error_type` varchar(100) DEFAULT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""