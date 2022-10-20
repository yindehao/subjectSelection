# _*_ coding: utf-8 _*_
"""
Time:     2022/10/19 15:24
Author:   Yin Dehao
Version:  V 1.0
File:     student_view
"""
import json

from flask import Blueprint, render_template, request, g, redirect, url_for, flash, session, jsonify
from werkzeug.security import check_password_hash

from common.ext import db
from models import Student
import pickle

bp = Blueprint("sbp", __name__, url_prefix='/student')


@bp.route('/')
def index():
    student_id = session['student_id']
    student = db.session.query(Student).filter_by(student_id=student_id).first()
    context = {'student': student}
    return render_template('student.html', **context)


@bp.route('/login', methods=['POST'])
def login():
    form = request.json
    username = form['username']
    password = form['password']
    student = db.session.query(Student).filter_by(student_id=username).first()
    if student and check_password_hash(student.password, password):
        data = row2dict(student)
        data['code'] = '200'
        print(data)
        # todo 解决类对象无法序列化的问题
        return jsonify(data)
    else:
        return jsonify({'code': 400})


# 数据库类对象转为字典
def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d


# 用户信息界面
@bp.route('/info')
def info():
    student_id = session['student_id']
    student = db.session.query(Student).filter_by(student_id=student_id).first()
    context = {'student': student}
    return render_template('student_info.html', **context)


# 课题市场界面
@bp.route('/subject_market')
def subject_market():
    pass


# 题目愿望单
@bp.route('/wish_list')
def wish_list():
    pass


# 组队界面
@bp.route('/group_work')
def group_work():
    pass


# 消息界面
@bp.route('/message')
def message():
    pass
