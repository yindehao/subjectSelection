# _*_ coding: utf-8 _*_
"""
Time:     2022/10/22 12:45
Author:   Yin Dehao
Version:  V 1.0
File:     row2dict
"""


# 工具函数
# 数据库类对象转为字典
def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d
