# _*_ coding: utf-8 _*_
"""
Time:     2022/10/15 20:51
Author:   Yin Dehao
Version:  V 1.0
File:     ext.py
"""
# 从此模块访问数据库
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()
cors = CORS()
