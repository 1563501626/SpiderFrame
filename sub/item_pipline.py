# -*- coding: utf-8 -*-
from DBUtils.PooledDB import PooledDB
import pymysql


class Database:
    def __init__(self, engine):
        self.engine = engine

    def sql_connection(self):
        sql_pool = PooledDB(creator=pymysql, host=self.engine.sql_host, user=self.engine.sql_user, passwd=self.engine.sql_pwd,
                            db=self.engine.sql_db, port=self.engine.sql_port)
        cursour = sql_pool.connection()
        if cursour:
            return cursour
        else:
            raise
