# -*- coding: utf-8 -*-
from DBUtils.PooledDB import PooledDB
import pymysql
import config


class Database:
    def __init__(self, engine):
        self.engine = engine

    def db_pool(self, sql_host=None, sql_user=None, sql_pwd=None, sql_db=None, sql_port=3306):
        if sql_host:
            sql_conn = pymysql.connect(host=sql_host, user=sql_user, password=sql_pwd, database=sql_db, port=sql_port,
                                       charset='utf8mb4')
            return sql_conn
        else:
            sql_pool = PooledDB(creator=pymysql, host=self.engine.sql_host, user=self.engine.sql_user, passwd=self.engine.sql_pwd,
                                db=self.engine.sql_db, port=self.engine.sql_port, mincached=1, maxcached=10)

            if sql_pool:
                return sql_pool
            else:
                raise

    def select_sql(self, table, select='*', where=None, one=False, cursor=None, sql=None, term=''):
        """查询"""
        conn = None
        select = str(select).replace("'", '')
        if not cursor:
            pool = self.engine.pool
            conn = pool.connection()
            cursor = conn.cursor()
        if not sql:
            if where:
                sql = f"select {select} from {table} where {where} " + term
            else:
                sql = f"select {select} from {table} " + term
        cursor.execute(sql)
        col_sql = f"select COLUMN_NAME from information_schema.COLUMNS where table_name = '{table}'"
        if one:
            ret = cursor.fetchone()
        else:
            ret = cursor.fetchall()
        if not ret:
            return None
        if select == '*':
            cursor.execute(col_sql)
            columns = cursor.fetchall()
            columns = list(map(lambda x: x[0], columns))
        else:
            columns = select.split(',')
        if conn:
            cursor.close()
            conn.close()
        if one:
            ret = [ret]
        ret = list(map(lambda x: dict(zip(columns, x)), ret))
        if len(ret) == 1:
            return ret[0]
        return ret

    def in_sql(self, table, names: tuple, values: tuple, cursor=None, sql=None):
        """入库"""
        conn = None
        print("入库：", dict(zip(names, values)))
        names = str(names).replace("'", '')
        values = str(values)
        if not cursor:
            pool = self.engine.pool
            conn = pool.connection()
            cursor = conn.cursor()
        if not sql:
            sql = f"insert into {table} {names} values {values} "
        cursor.execute(sql)
        if conn:
            conn.commit()
            cursor.close()
            conn.close()

    def update_sql(self, table, names: tuple, values: tuple, where, cursor=None, sql=None):
        """更新"""
        conn = None
        temp = zip(names, values)
        ret = ','.join(list(map(lambda x: f"{x[0]}='{x[1]}'", list(temp))))
        if not cursor:
            pool = self.engine.pool
            conn = pool.connection()
            cursor = conn.cursor()
        if not sql:
            sql = f"update {table} set {ret} where {where} "
        cursor.execute(sql)
        if conn:
            conn.commit()
            cursor.close()
            conn.close()

    def update_spider_info(self, names, values, queue_name):
        """更新爬虫信息"""
        conn = self.db_pool(sql_host=config.spider_host, sql_user=config.spider_user, sql_pwd=config.spider_pwd,
                            sql_db=config.spider_db, sql_port=config.spider_port)
        cursor = conn.cursor()
        self.update_sql(config.spider_table, names, values, where=f'queue_name="{queue_name}"', cursor=cursor)
        conn.commit()
        cursor.close()
        conn.close()
