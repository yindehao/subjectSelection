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
    query_wish_list_by_team_id, query_team_by_id, query_student_by_team_id, create_team_by_leader, \
    delete_team_by_team_id, update_team_name, join_team_by_team_id, query_team_full_by_id, withdraw_team_by_student_id
from models import Student, Subject, ReleaseSubject, Dept, Team
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


# 根据id查询学生信息
@bp.route('/id/<student_id>')
def query_by_id(student_id):
    try:
        student = query_student_by_id(student_id)
        return jsonify(code=200, msg='找到学生', data=row2dict(student))
    except TypeError as error:
        return jsonify(code=400, msg='找不到学生', data={})


# 根据姓名模糊查找学生信息
@bp.route('/name/<student_name>')
def query_by_name(student_name):
    try:
        student = query_student_by_name(student_name)
        return jsonify(code=200, msg='找到学生', data=row2dict(student))
    except TypeError as error:
        return jsonify(code=400, msg='找不到学生', data={})


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


# 用户信息界面 获取个人信息和修改个人信息
@bp.route('/info', methods=['GET', 'POST'])
def info():
    try:
        if request.method == 'GET':
            student_id = session['student_id']
            student = query_student_by_id(student_id)
            data = row2dict(student)
            return jsonify(code='200', data=data, msg='找到学生信息')
        # 更改信息
        else:
            form = request.json
            student_id = form['username']
            student = query_student_by_id(student_id)
            dept = query_dept_by_id(student.dept_id)
            # 可能修改的字段：手机号，邮箱，生日，自我介绍
            student.phone_number = form['TELE']
            student.email = form['Email']
            student.birthday = form['birthday'][0:10]
            student.description = form['description']
            db.session.commit()
            data = row2dict(student)
            data['dept_name'] = dept.dept_name
            return jsonify(code='200', data=data, msg='修改信息成功')
    except AttributeError as err:
        return jsonify(code='400', data=dict(), msg='查找不到用户信息')
    except TypeError as err:
        return jsonify(code='400', data=dict(), msg='查找不到用户信息')


# 获取题目愿望单
@bp.route('/wish_list/<student_id>')
def query_wish_list(student_id):
    try:
        student = query_student_by_id(student_id)
        team_id = student.team_id
        if team_id:
            data = dict()
            wish_list = query_wish_list_by_team_id(team_id)
            print(wish_list)
            data_keys = ['join_time','subject_id', 'subject_name', 'language', 'instructor_name',
                         'origin', 'min_person', 'max_person', 'max_group']
            for wish in wish_list:
                data[wish.subject_id] = dict()
                for key_index in range(len(data_keys) - 1):
                    logging.debug(wish[key_index])
                    data[wish.subject_id][data_keys[key_index]] = wish[key_index]
            return jsonify(code='200', data=data, msg='成功获取愿望单')
        else:
            return jsonify(code='401', data=dict(), msg='请先创建小组或者加入小组')
    except AttributeError as err:
        logging.warning(err)
        return jsonify(code='402', data=dict(), msg='查找不到用户信息')
    except RuntimeError as err:
        logging.warning(err)
        return jsonify(code='403', data=dict(), msg='查找不到用户信息')


# get小组信息，post修改小组，put创建小组，delete删除小组
@bp.route('/team/<student_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def team_work(student_id):
    try:
        student = query_student_by_id(student_id)
        # 查询小组和小组成员
        if request.method == 'GET':
            if student.team_id:
                data = query_team_full_by_id(student.team_id)
                return jsonify(code='200', msg='找到小组内的学生信息', data=data)
            else:
                return jsonify(code='401', msg='学生尚未组队', data=dict())
        # PUT创建小组
        # 提交表单：{'team_name':{team_name}}
        elif request.method == 'PUT':
            if student.team_id is None:
                form = request.json
                team_name = form['team_name']
                team = create_team_by_leader(student_id, team_name)
                db.session.commit()
                student.team_id = team.team_id
                db.session.commit()
                return jsonify(code='200', msg='创建小组成功', data=row2dict(team))
            else:
                return jsonify(code='402', msg='请先退出小组', data=dict())
        # 删除小组，只有队长才可以
        elif request.method == 'DELETE':
            if student.team_id:
                team = query_team_by_id(student.team_id)
                # 如果是队长
                if team.leader_id == student.student_id:
                    result = delete_team_by_team_id(team.team_id)
                    if result:
                        return jsonify(code='200', msg='删除小组成功', data=dict())
                    else:
                        return jsonify(code='403', msg='删除小组失败', data=dict())
                else:
                    return jsonify(code='404', msg='当前用户没有删除小组的权限', data=dict())
            else:
                return jsonify(code='405', msg='当前用户没有加入或者创建小组', data=dict())
        # POST方法 修改小组名称
        # 提交表单：{'team_name':{team_name}}
        else:
            if student.team_id:
                team = query_team_by_id(student.team_id)
                # 如果是队长
                if team.leader_id == student.student_id:
                    team_name = request.json['team_name']
                    update_team_name(team.team_id, team_name)
                    return jsonify(code='200', msg='修改小组成功', data=dict())
                else:
                    return jsonify(code='404', msg='当前用户修改小组的权限', data=dict())
    except TypeError as err:
        return jsonify(code='400', msg='找不到学生信息')


# 按照组长或者组员的学号搜索小组
# ?student_id=<student_id>
@bp.route('/team', methods=['GET'])
def search_team_by_id():
    try:
        student_id = request.args.get('student_id')
        student = query_student_by_id(student_id)
        team = query_team_by_id(student.team_id)
        team_leader = query_student_by_id(team.leader_id)
        data = row2dict(team)
        data['team_leader'] = team_leader.student_name
        return jsonify(code='200', data=data, msg='成功找到小组')
    except Exception as err:
        return jsonify(code='400', data=dict(), msg='找不到小组')


# 按照组长或者组员的姓名搜索小组
# student_name=<student_name>
@bp.route('/teams', methods=['GET'])
def search_team_by_name():
    try:
        student_name = request.args.get('student_name')
        students = query_student_by_name(student_name)
        data = dict()
        for student in students:
            team = query_team_by_id(student.team_id)
            team_leader = query_student_by_id(team.leader_id)
            data[team.team_id] = row2dict(team)
            data[team.team_id]['team_leader'] = team_leader.student_name
        return jsonify(code='200', data=data, msg='成功找到小组')
    except Exception as err:
        return jsonify(code='400', msg='找不到小组')


# 加入
@bp.route('/team/<student_id>/join', methods=['POST'])
def join_team_by_id(student_id):
    try:
        team_id = request.json['team_id']
        student = query_student_by_id(student_id)
        if student.team_id is None:
            join_team_by_team_id(student_id, team_id)
            data = query_team_full_by_id(team_id)
            return jsonify(code='200', data=data, msg='成功加入小组')
        else:
            return jsonify(code='400', data=dict(), msg='请先退出小组')
    except Exception as e:
        return jsonify(code='400', data=dict(), msg='无法加入小组')


# 退出小组
@bp.route('/team/<student_id>/quit', methods=['POST'])
def quit_team_by_id(student_id):
    try:
        student = query_student_by_id(student_id)
        if student.team_id:
            withdraw_team_by_student_id(student_id)
            return jsonify(code='200', data=row2dict(student), msg='成功退出小组')
        else:
            return jsonify(code='400', data=dict(), msg='请先加入小组')
    except Exception as e:
        return jsonify(code='400', data=dict(), msg='无法加入小组')


# 消息界面
@bp.route('/message')
def message():
    pass
