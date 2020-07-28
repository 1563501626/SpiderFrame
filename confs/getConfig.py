import configparser
from fuclib import ezfuc
import os
from fuclib import MySql
import config


class MyConfigParser(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


def get_config():
    return config


def company_name_db():
    gConfig = get_config()
    host = gConfig.sql_host
    username = gConfig.sql_user
    password = gConfig.sql_pwd
    database = "company"
    port = int(gConfig.sql_port)
    db = MySql(host, database, username, password, port)  # 企业名录所在库、表
    return db


def conn(database):
    gConfig = get_config()
    host = gConfig['hostname']
    username = gConfig['user']
    password = gConfig['password']
    port = int(gConfig['port'])
    db = MySql(host, database, username, password, port)
    return db