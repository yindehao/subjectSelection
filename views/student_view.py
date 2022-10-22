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
from werkzeug.security import check_password_hash, generate_password_hash

from common.ext import db
from common.row2dict import row2dict
from controller.student_controller import query_student_by_name, query_student_by_id, query_dept_by_id, \
    query_wish_list_by_team_id
from models import Student, Subject, ReleaseSubject, Dept
import pickle

bp = Blueprint("sbp", __name__, url_prefix='/student')


# 后端测试函数
@bp.route('/')
def index():
    student_id = session['student_id']
    try:
        student = db.session.query(Student).filter_by(student_id=student_id).first()
        context = {'student': row2dict(student)}
        return render_template('student.html', **context)
    except TypeError as err:
        return jsonify(code='400', msg=f'学号 {student_id} 不存在系统中')


# 学生登录表单
@bp.route('/login', methods=['POST'])
def login():
    form = request.json
    student_id = form['username']
    password = form['password']
    try:
        student = query_student_by_id(student_id)
        dept = query_dept_by_id(Student.dept_id)
        # 如果密码和加密后的密码匹配，则返回登录信息
        if student and check_password_hash(student.password, password):
            data = row2dict(student)
            data['dept_name'] = dept.dept_name
            session['student_id'] = student_id
            return jsonify(code='200', data=data, msg='学号和密码匹配')
        # 如果是明文导入的密码，更改为哈希后的密码
        elif student and student.password == password:
            student.password = generate_password_hash(password)
            db.session.commit()
            data = row2dict(student)
            data['dept_name'] = dept.dept_name
            session['student_id'] = student_id
            return jsonify(code='200', data=data, msg='学号和密码匹配')
        else:
            return jsonify(code='400', msg='学号或者密码错误！')
    # 该学号不存在
    except TypeError as err:
        return jsonify(code='400', msg=f'学号 {student_id} 不存在系统中')


# 用户信息界面 获取个人信息
@bp.route('/info', methods=['GET', 'POST'])
def info():
    if request.method == 'GET':
        student_id = session['student_id']
        student = db.session.query(Student).filter_by(student_id=student_id).first()
        data = row2dict(student)
        return jsonify(code='200', data=data, msg='找到学生信息')
    # 更改信息
    else:
        form = request.json
        print(form)
        student = db.session.query(Student).filter_by(student_id=form['username']).first()
        student.phone_number = form['TELE']
        student.email = form['Email']
        student.birthday = form['birthday'][0:10]
        # todo 前后端选择日期差一天
        student.description = form['description']
        db.session.commit()
        dept = query_dept_by_id(student.dept_id)
        data = row2dict(student)
        data['dept_name'] = dept.dept_name
        return jsonify(code='200', data=data, msg='修改信息成功')


# 题目愿望单
@bp.route('/wish_list/<student_id>')
def query_wish_list(student_id):
    try:
        student = query_student_by_id(student_id)
        team_id = student.team_id
        if team_id:
            wish_list = query_wish_list_by_team_id(team_id)
        else:
            return jsonify(code='400',msg='请先创建小组或者加入小组')
    except TypeError as err:
        pass
    pass


# 组队界面
@bp.route('/group_work')
def group_work():
    pass


# 消息界面
@bp.route('/message')
def message():
    pass


# 根据id查询学生信息
@bp.route('/id/<student_id>')
def query_by_id(student_id):
    try:
        student = query_student_by_id(student_id)
        return jsonify(code=200, msg='找到学生', data=row2dict(student))
    except TypeError as error:
        return jsonify(code=400, msg='找不到学生', data={})


# 根据姓名查找学生信息
@bp.route('/name/<student_name>')
def query_by_name(student_name):
    try:
        student = query_student_by_name(student_name)
        return jsonify(code=200, msg='找到学生', data=row2dict(student))
    except TypeError as error:
        return jsonify(code=400, msg='找不到学生', data={})
