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
from .student_view import index as student_index
from .instructor_view import index as instructor_index


