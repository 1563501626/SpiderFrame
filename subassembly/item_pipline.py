# -*- coding: utf-8 -*-
from DBUtils.PooledDB import PooledDB
import pymysql


def sql_connection(engine):
    sql_pool = PooledDB(creator=pymysql, host=engine.sql_host, user=engine.sql_user, passwd=engine.sql_pwd,
                        db=engine.sql_db, port=engine.sql_port)
