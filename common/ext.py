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
from flask_mail import Mail

# 开启数据库
# 跨域资源共享，前端向后端发送资源请求
# 邮箱服务，用来发送请求邮件
db = SQLAlchemy()
cors = CORS()
mail = Mail()
