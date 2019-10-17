# -*- coding: utf-8 -*-
import config


class Engine:
    def __init__(self):
        self.mq_host = None
        self.mq_port = None
        self.mq_user = None
        self.mq_pwd = None
        self.sql_host = None
        self.sql_port = None
        self.sql_user = None
        self.sql_pwd = None

    def init(self):
        """初始化"""
        self.mq_host = config.mq_host
        self.mq_port = config.mq_port
        self.mq_user = config.mq_user
        self.mq_pwd = config.mq_pwd
        self.sql_host = config.sql_host
        self.sql_port = config.sql_port
        self.sql_user = config.sql_user
        self.sql_pwd = config.sql_pwd

        serious = ['mq_host', 'mq_port', 'mq_user', 'mq_pwd', 'sql_host', 'sql_port', 'sql_user', 'sql_pwd']
        for i in serious:
            pass


if __name__ == '__main__':
    e = Engine()
    e.init()