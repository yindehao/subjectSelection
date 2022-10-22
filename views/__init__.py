# _*_ coding: utf-8 _*_
"""
Time:     2022/10/16 15:24
Author:   Yin Dehao
Version:  V 1.0
File:     __init__.py
"""
# 这里存放路由蓝图文件
from .student_view import bp as student_bp
from .instructor_view import bp as instructor_bp
from .subject_view import bp as subject_bp
from .student_view import index as student_index
from .instructor_view import index as instructor_index


# 工具函数
# 数据库类对象转为字典
def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d
