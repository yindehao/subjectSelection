# _*_ coding: utf-8 _*_
"""
Time:     2022/10/22 12:45
Author:   Yin Dehao
Version:  V 1.0
File:     row2dict
"""
import time


# 工具函数
# 数据库类对象转为字典
def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d


# 获取本地时间
def get_local_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# 根据开发和发布，返回不同的ip地址
def host_ip(dev):
    if dev:
        return '127.0.0.1'
    else:
        return '47.92.33.188'


# 端口号
def host_port():
    return 5000
