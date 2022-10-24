# _*_ coding: utf-8 _*_
"""
Time:     2022/10/15 20:52
Author:   Yin Dehao
Version:  V 1.0
File:     config
"""
# 数据库的配置信息
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'subject_selection_db'
USERNAME = 'root'
PASSWORD = 'dut201892487'  # todo 更改为你的root用户密码
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = "ustc20221015"

JSON_AS_ASCII = False
