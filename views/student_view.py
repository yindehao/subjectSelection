# _*_ coding: utf-8 _*_
"""
Time:     2022/10/19 15:24
Author:   Yin Dehao
Version:  V 1.0
File:     student_view
"""
import json
import logging

from flask import Blueprint, render_template, request, g, redirect, url_for, flash, session, jsonify
from werkzeug.security import check_password_hash

from common.ext import db
from models import Student, Subject, ReleaseSubject
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
    student_id = form['username']
    password = form['password']
    session['student_id'] = student_id
    student = db.session.query(Student).filter_by(student_id=student_id).first()
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


# 用户信息界面 获取个人信息
@bp.route('/info', methods=['GET', 'POST'])
def info():
    student_id = session['student_id']
    student = db.session.query(Student).filter_by(student_id=student_id).first()
    if request.method == 'GET':
        data = row2dict(student)
        data['code'] = '200'
        return jsonify(data)
    # 更改信息
    else:
        # update student info
        form = request.json
        # form为提交的表单内容 student_new 为更改后的学生信息
        for key in form.keys():
            # 更改学生信息
            setattr(student, key, form[key])
            # 打印日志
            logging.warning(f'student {student.name}\'s {key} changed to {form[key]} ')
        db.session.commit()
        data = row2dict(student)
        data['code'] = '200'
        return jsonify(data)


# 课题市场界面
@bp.route('/subject_market', methods=['GET', 'POST'])
def subject_market():
    # if get
    # 查询所有已经发布的课题
    subjects = db.session.query(Subject, ReleaseSubject).join(ReleaseSubject).filter_by(
        ReleaseSubject.released).limit(20, 0).all()
    data = dict()
    for subject in subjects:
        subject_data = row2dict(subject)
        data[subject.subject_id] = subject_data
    data['code'] = '200'
    return jsonify(data)


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
