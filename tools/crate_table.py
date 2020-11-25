from fuclib import MySql

import config

database = "zlcollector_cost"


host = config.sql_host
username = config.sql_user
password = config.sql_pwd
port = 3306
db = MySql(host, database, username, password, port)
db.query("""
CREATE TABLE `spider_update` (
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
""")