# _*_ coding: utf-8 _*_
"""
Time:     2022/10/19 15:24
Author:   Yin Dehao
Version:  V 1.0
File:     student_view
"""
import logging
from flask import Blueprint, render_template, request, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from common import config
from common.ext import db, mail
from common.utils2 import row2dict, host_ip, host_port
import controller.student_controller
from controller.subject_controller import query_subject_by_id
from models import Student
from flask_mail import Message

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
        return jsonify(code=400, msg=f'学号 {student_id} 不存在系统中')


# 根据id查询学生信息、创建学生信息、删除学生信息
@bp.route('/id/<student_id>', methods=['GET'])
def query_by_id(student_id):
    try:
        student = controller.student_controller.query_student_by_id(student_id)
        dept = controller.student_controller.query_dept_by_id(Student.dept_id)
        data = row2dict(student)
        data['dept_name'] = dept.dept_name
        return jsonify(code=200, msg='找到学生', data=data)
    except Exception as error:
        logging.warning(error)
        return jsonify(code=400, msg='找不到学生', data={})


# 根据姓名模糊查找学生信息
@bp.route('/name/<student_name>')
def query_by_name(student_name):
    try:
        students = controller.student_controller.query_student_by_name(student_name)
        data = dict()
        for student in students:
            data[student.student_id] = row2dict(student)
            dept = controller.student_controller.query_dept_by_id(Student.dept_id)
            data[student.student_id]['dept_name'] = dept.dept_name
        if data:
            return jsonify(code=200, msg='找到学生', data=data)
        else:
            return jsonify(code=400, msg='找不到学生', data=data)
    except Exception as error:
        logging.warning(error)
        return jsonify(code=400, msg='找不到学生', data={})


# 学生登录表单
@bp.route('/login', methods=['POST'])
def login():
    form = request.json
    student_id = form['username']
    password = form['password']
    try:
        student = controller.student_controller.query_student_by_id(student_id)
        dept = controller.student_controller.query_dept_by_id(Student.dept_id)
        # 如果密码和加密后的密码匹配，则返回登录信息
        if student and check_password_hash(student.password, password):
            data = row2dict(student)
            data['dept_name'] = dept.dept_name
            session['student_id'] = student_id
            return jsonify(code=200, data=data, msg='学号和密码匹配')
        # 如果是明文导入的密码，更改为哈希后的密码
        elif student and student.password == password:
            student.password = generate_password_hash(password)
            db.session.commit()
            data = row2dict(student)
            data['dept_name'] = dept.dept_name
            session['student_id'] = student_id
            return jsonify(code=200, data=data, msg='学号和密码匹配')
        else:
            return jsonify(code=400, msg='学号或者密码错误！')
    # 该学号不存在
    except Exception as err:
        logging.warning(err)
        return jsonify(code=400, msg=f'学号 {student_id} 不存在系统中')


# 用户信息界面 获取个人信息和修改个人信息
@bp.route('/info', methods=['GET', 'POST'])
def info():
    try:
        if request.method == 'GET':
            student_id = session['student_id']
            student = controller.student_controller.query_student_by_id(student_id)
            data = row2dict(student)
            return jsonify(code=200, data=data, msg='找到学生信息')
        # 更改信息
        else:
            form = request.json
            student_id = form['username']
            student = controller.student_controller.query_student_by_id(student_id)
            dept = controller.student_controller.query_dept_by_id(student.dept_id)
            # 可能修改的字段：手机号，邮箱，生日，自我介绍
            student.phone_number = form['TELE']
            student.email = form['Email']
            student.birthday = form['birthday'][0:10]
            student.description = form['description']
            db.session.commit()
            data = row2dict(student)
            data['dept_name'] = dept.dept_name
            return jsonify(code=200, data=data, msg='修改信息成功')
    except AttributeError as err:
        return jsonify(code=400, data=dict(), msg='查找不到用户信息')
    except Exception as err:
        logging.warning(err)
        return jsonify(code=400, data=dict(), msg='查找不到用户信息')


'''
愿望单接口信息
'''


# 获取题目愿望单 GET
# 加入愿望单 PUT
# 删除愿望单 DELETE
@bp.route('/wish_list/<int:team_id>', methods=['GET', 'PUT', 'DELETE'])
def wish_list(team_id):
    try:
        if request.method == 'GET':
            return query_wish_list(team_id=team_id)
        elif request.method == 'PUT':
            team_id = int(team_id)
            subject_id = request.json['subject_id']
            return add_wish_list(team_id=team_id, subject_id=subject_id)
        else:
            team_id = int(team_id)
            subject_id = request.json['subject_id']
            return delete_from_wish_list(team_id=team_id, subject_id=subject_id)
    except Exception as err:
        logging.warning(err)
        return jsonify(code=400, data=dict(), msg='找不到小组')


# 查询愿望单
def query_wish_list(team_id):
    try:
        if team_id:
            data = dict()
            wishes = controller.student_controller.query_wish_list_by_team_id(team_id)
            print(wishes)
            data_keys = ['subject_id', 'subject_name', 'language', 'instructor_name',
                         'origin', 'min_person', 'max_person', 'max_group', 'join_time']
            for wish in wishes:
                data[wish.subject_id] = dict()
                for key_index in range(len(data_keys)):
                    logging.debug(wish[key_index])
                    data[wish.subject_id][data_keys[key_index]] = wish[key_index]
            return jsonify(code=200, data=data, msg='成功获取愿望单')
        else:
            return jsonify(code=401, data=dict(), msg='请先创建小组或者加入小组')
    except AttributeError as err:
        logging.warning(err)
        return jsonify(code=402, data=dict(), msg='查找不到用户信息')
    except RuntimeError as err:
        logging.warning(err)
        return jsonify(code=403, data=dict(), msg='查找不到用户信息')


# 删除愿望单
def delete_from_wish_list(team_id, subject_id):
    try:
        wish = controller.student_controller.query_wish_by_id(team_id, subject_id)
        subject = query_subject_by_id(subject_id)
        if wish:
            controller.student_controller.delete_wish_list(team_id, subject_id)
            return jsonify(code=200, data=dict(), msg=f'成功删除标题为{subject.subject_name} 的愿望')
        else:
            return jsonify(code=400, data=dict(), msg=f'愿望单中没有标题为{subject.subject_name} 的愿望')
    except Exception as err:
        logging.warning(err)
        return jsonify(code=400, data=dict(), msg='找不到课题')


# 添加愿望单
def add_wish_list(team_id, subject_id):
    try:
        wish = controller.student_controller.query_wish_by_id(team_id, subject_id)
        subject = query_subject_by_id(subject_id)
        if wish is None:
            controller.student_controller.add_2_wish_list(team_id, subject_id)
            db.session.commit()
            return jsonify(code=200, data=dict(), msg=f'成功将标题为{subject.subject_name}加入愿望单')
        else:
            return jsonify(code=400, data=dict(), msg=f'您已经添加过标题为{subject.subject_name}的课题了')
    except Exception as err:
        logging.warning(err)
        return jsonify(code=400, data=dict(), msg='找不到课题')


'''
小组信息
'''


# get小组信息，post修改小组，put创建小组，delete删除小组
@bp.route('/team/<student_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def team_work(student_id):
    try:
        student = controller.student_controller.query_student_by_id(student_id)
        # 查询小组和小组成员
        if request.method == 'GET':
            if student.team_id:
                data = controller.student_controller.query_team_full_by_id(student.team_id)
                return jsonify(code=200, msg='找到小组内的学生信息', data=data)
            else:
                return jsonify(code=401, msg='学生尚未组队', data=dict())
        # PUT创建小组
        # 提交表单：{'team_name':{team_name}}
        elif request.method == 'PUT':
            if student.team_id is None:
                form = request.json
                team_name = form['team_name']
                team = controller.student_controller.create_team_by_leader(student_id, team_name)
                db.session.commit()
                student.team_id = team.team_id
                db.session.commit()
                return jsonify(code=200, msg='创建小组成功', data=row2dict(team))
            else:
                return jsonify(code=402, msg='请先退出小组', data=dict())
        # 删除小组，只有队长才可以
        elif request.method == 'DELETE':
            if student.team_id:
                team = controller.student_controller.query_team_by_id(student.team_id)
                # 如果是队长
                if team.leader_id == student.student_id:
                    result = controller.student_controller.delete_team_by_team_id(team.team_id)
                    if result:
                        return jsonify(code=200, msg='删除小组成功', data=dict())
                    else:
                        return jsonify(code=403, msg='删除小组失败', data=dict())
                else:
                    return jsonify(code=404, msg='当前用户没有删除小组的权限', data=dict())
            else:
                return jsonify(code=405, msg='当前用户没有加入或者创建小组', data=dict())
        # POST方法 修改小组名称
        # 提交表单：{'team_name':{team_name}}
        else:
            if student.team_id:
                team = controller.student_controller.query_team_by_id(student.team_id)
                # 如果是队长
                if team.leader_id == student.student_id:
                    team_name = request.json['team_name']
                    controller.student_controller.update_team_name(team.team_id, team_name)
                    return jsonify(code=200, msg='修改小组成功', data=dict())
                else:
                    return jsonify(code=400, msg='当前用户无修改小组的权限', data=dict())
    except Exception as err:
        logging.warning(err)
        return jsonify(code=400, msg='找不到学生信息', data=dict())


# 按照组长或者组员的学号搜索小组
# ?student_id=<student_id>
@bp.route('/team', methods=['GET'])
def search_team_by_id():
    try:
        student_id = request.args.get('student_id')
        student = controller.student_controller.query_student_by_id(student_id)
        # data = controller.student_controller.query_team_full_by_id(student.team_id)
        team = controller.student_controller.query_team_by_id(student.team_id)
        team_data = row2dict(team)
        team_leader = controller.student_controller.query_student_by_id(team.leader_id)
        team_data['team_leader'] = team_leader.student_name
        data = list()
        data.append(team_data)
        return jsonify(code=200, data=data, msg='成功找到小组')
    except Exception as err:
        logging.warning(err)
        return jsonify(code=400, data=dict(), msg='找不到小组')


# 按照组长或者组员的姓名搜索小组
# student_name=<student_name>
@bp.route('/teams', methods=['GET'])
def search_team_by_name():
    try:
        student_name = request.args.get('student_name')
        students = controller.student_controller.query_student_by_name(student_name)
        data = list()
        for student in students:
            team = controller.student_controller.query_team_by_id(student.team_id)
            team_leader = controller.student_controller.query_student_by_id(team.leader_id)
            team_data = row2dict(team)
            team_data['team_leader'] = team_leader.student_name
            data.append(team_data)
        if data:
            return jsonify(code=200, data=data, msg='成功找到小组')
        else:
            return jsonify(code=400, data=dict(), msg='找不到小组')
    except Exception as err:
        logging.warning(err)
        return jsonify(code=400, data=dict(), msg='找不到小组')


# 加入
@bp.route('/team/<student_id>/join', methods=['POST'])
def join_team_by_id(student_id):
    try:
        team_id = request.json['team_id']
        student = controller.student_controller.query_student_by_id(student_id)
        team = controller.student_controller.query_team_by_id(team_id)
        team_leader = controller.student_controller.query_student_by_id(team.leader_id)
        logging.warning(team_leader)
        if student.team_id is None:
            if controller.student_controller.query_team_count(team_id) < 4:
                # 申请通过后，才真正接受请求
                if not controller.student_controller.query_apply_join(team_id=team_id, student_id=student_id):
                    controller.student_controller.add_apply_join(team_id=team_id, student_id=student_id)
                msg = write_join_email(leader=team_leader, student=student, team_name=team.team_name)

                mail.send(msg)
                # controller.student_controller.join_team_by_team_id(student_id, team_id)
                data = controller.student_controller.query_team_full_by_id(team_id)
                return jsonify(code=200, data=data, msg='已经发送加入请求，请等待队长通过')
            else:
                return jsonify(code=401, data=dict(), msg='小组已经满了')
        else:
            return jsonify(code=400, data=dict(), msg='请先退出小组')
    except Exception as e:
        logging.warning(e)
        return jsonify(code=400, data=dict(), msg='无法加入小组')


# 退出小组
@bp.route('/team/<student_id>/quit', methods=['POST'])
def quit_team_by_id(student_id):
    try:
        student = controller.student_controller.query_student_by_id(student_id)
        if student.team_id:
            controller.student_controller.withdraw_team_by_student_id(student_id)
            return jsonify(code=200, data=row2dict(student), msg='成功退出小组')
        else:
            return jsonify(code=400, data=dict(), msg='请先加入小组')
    except Exception as e:
        logging.warning(e)
        return jsonify(code=400, data=dict(), msg='无法退出小组')


# 查看加入小组的结果
@bp.route('/team/<student_id>/join_team', methods=['GET'])
def join_result(student_id):
    try:
        student = controller.student_controller.query_student_by_id(student_id)
        if student.team_id:
            applies = controller.student_controller.query_apply_join_by_team(team_id=student.team_id)
            data = list()
            for apply in applies:
                data.append(row2dict(apply))
            return jsonify(code=200, data=data, msg='成功获得加入小组申请')
        else:
            return jsonify(code=400, data=dict(), msg='请先加入小组')
    except Exception as err:
        logging.warning(err)
        return jsonify(code=400, data=dict(), msg='无法获取选中课题信息')


# 发送邮件
def write_join_email(leader, student, team_name):
    msg = Message()
    msg.sender = config.MAIL_DEFAULT_SENDER
    msg.recipients = [leader.email, config.MAIL_DEFAULT_RECIPIENT]
    msg.subject = f'加入小组请求：{student.student_id}{student.student_name}想要加入您的小组({team_name})'
    # 与操作
    key1 = generate_password_hash(leader.password)
    key2 = generate_password_hash(leader.password)
    context = {
        'leader': leader,
        'student': student,
        'team_name': team_name,
        'accept_join': f'http://{host_ip(config.SSS_DEV)}:{host_port()}/student/team/accept?'
                       f'leader_id={leader.student_id}&participant_id={student.student_id}'
                       f'&accessor={key1}',
        "refuse_join": f'http://{host_ip(config.SSS_DEV)}:{host_port()}/student/team/refuse?'
                       f'leader_id={leader.student_id}&participant_id={student.student_id}'
                       f'&accessor={key2}',
    }
    msg.html = render_template("申请加入小组.html", **context)
    return msg


@bp.route('/team/accept', methods=['POST'])
def accept_join_mail():
    try:

        leader_id = request.args.get('leader_id')
        participant_id = request.args.get('participant_id')
        key1 = request.args.get('accessor')

        leader = controller.student_controller.query_student_by_id(leader_id)
        participant = controller.student_controller.query_student_by_id(participant_id)
        # 如果access不正确
        if not check_password_hash(key1, leader.password):
            return '错误的URL格式'
        # 如果人数不够，加入后不到4人
        if controller.student_controller.query_team_count(leader.team_id) < 3:
            controller.student_controller.update_apply_join(leader.team_id, participant_id, True)
            participant.team_id = leader.team_id
            db.session.commit()
            return '您已经同意该成员加入您的小组'
        # 如果还有其他申请，且队伍中没有剩余位置
        elif controller.student_controller.query_team_count(leader.team_id) == 3:
            applies = controller.student_controller.query_apply_join_by_team(leader.team_id)
            for apply in applies:
                # 拒绝其他申请
                if apply.version == 1:
                    controller.student_controller.update_apply_join(leader.team_id, apply.participant_id, False)
            db.session.commit()
            return '加入该成员后，您的小组已经满员，已拒绝其他申请'
        # 申请已经满了
        else:
            return '小组已经满员，无法通过申请'
    except Exception as err:
        logging.warning(err)
        return '地址不正确'


@bp.route('/team/refuse', methods=['POST'])
def refuse_join_mail():
    try:
        leader_id = request.args.get('leader_id')
        participant_id = request.args.get('participant_id')
        key2 = request.args.get('accessor')
        leader = controller.student_controller.query_student_by_id(leader_id)
        # 如果access不正确
        if not check_password_hash(key2, leader.password):
            return '错误的URL格式'
        controller.student_controller.update_apply_join(leader.team_id, participant_id, False)
        return '您已经拒绝该成员加入您的小组'
    except Exception as err:
        logging.warning(err)
        return '地址不正确'


# 查看选题结果
@bp.route('/team/<student_id>/selected_subject', methods=['GET'])
def selected_subject(student_id):
    try:
        student = controller.student_controller.query_student_by_id(student_id)
        if student.team_id:
            applies = controller.student_controller.query_apply_select_by_team(team_id=student.team_id)
            data = list()
            for apply in applies:
                data.append(row2dict(apply))
            return jsonify(code=200, data=data, msg='成功获得选题申请')
        else:
            return jsonify(code=400, data=dict(), msg='请先加入小组')
    except Exception as err:
        logging.warning(err)
        return jsonify(code=400, data=dict(), msg='无法获取选中课题信息')


# 申请选题
@bp.route('/team/<student_id>/select', methods=['POST'])
def select_subject(student_id):
    try:
        student = controller.student_controller.query_student_by_id(student_id)
        subject_id = request.json['subject_id']
        if student.team_id:
            team = controller.student_controller.query_team_by_id(team_id=student.team_id)
            if team.leader_id == student.student_id:

                subject = controller.subject_controller.query_subject_by_id(subject_id=subject_id)
                # 已经选中课题的组数
                count = controller.student_controller.get_accept_apply_select_count(subject_id=subject_id)

                if subject.max_group > count:
                    if not controller.student_controller.query_apply_select(subject_id, team_id=student.team_id):
                        controller.student_controller.add_apply_select(subject_id=subject_id, team_id=student.team_id)
                    instructor = controller.subject_controller.query_instructor_by_subject_id(subject_id)
                    teammates = controller.student_controller.query_student_by_team_id(team_id=team.team_id)
                    msg = write_select_email(subject, instructor, team, teammates)
                    mail.send(msg)
                    return jsonify(code=200, data=dict(), msg='已经发送选课请求，请等待教师通过')
                else:
                    return jsonify(code=400, data=dict(), msg='选题小组已满')
            else:
                jsonify(code=401, data=dict(), msg='您不是小组组长，无法申请选题')
        else:
            return jsonify(code=402, data=dict(), msg='请先加入小组')
    except Exception as err:
        logging.warning(err)
        return jsonify(code=400, data=dict(), msg='无法选中课题')


def write_select_email(subject, instructor, team, teammates):
    msg = Message()
    msg.sender = config.MAIL_DEFAULT_SENDER
    #  暂时不用导师邮箱
    msg.recipients = [config.MAIL_DEFAULT_RECIPIENT]
    msg.subject = f'{instructor.instructor_name}您好：小组{team.team_name} 想要申请做您的课题({subject.subject_name})'
    # 与操作
    key1 = generate_password_hash(instructor.password)
    key2 = generate_password_hash(instructor.password)
    context = {
        'team': team,
        'instructor': instructor,
        'subject': subject,
        'teammates': teammates,
        'accept_join': f'http://{host_ip(config.SSS_DEV)}:{host_port()}/student/select/accept?'
                       f'subject_id={subject.subject_id}&team_id={team.team_id}'
                       f'&accessor={key1}',
        "refuse_join": f'http://{host_ip(config.SSS_DEV)}:{host_port()}/student/select/refuse?'
                       f'subject_id={subject.subject_id}&team_id={team.team_id}'
                       f'&accessor={key2}',
    }
    msg.html = render_template("申请选题.html", **context)
    return msg


@bp.route('/select/accept', methods=['POST'])
def accept_select_mail():
    try:
        subject_id = request.args.get('subject_id')
        team_id = request.args.get('team_id')
        key1 = request.args.get('accessor')
        team = controller.student_controller.query_team_by_id(team_id)
        subject = controller.subject_controller.query_subject_by_id(subject_id)
        instructor = controller.subject_controller.query_instructor_by_subject_id(subject_id)
        count = controller.student_controller.get_accept_apply_select_count(subject_id=subject_id)
        # 如果access不正确
        if not check_password_hash(key1, instructor.password):
            return '错误的URL格式'
        # 如果人数不够，加入后不到4人
        if count < subject.max_group - 1:
            controller.student_controller.update_apply_select(subject_id, team_id, True)
            team.subject_id = subject_id
            db.session.commit()
            return '您已经同意小组选中您的课题'
        # 如果还有其他申请，且没有剩余组数，将拒绝其他小组
        elif count == subject.max_group - 1:
            applies = controller.student_controller.query_apply_select(subject_id)
            for apply in applies:
                if apply.version == 1:
                    # 拒绝其他申请
                    controller.student_controller.update_apply_select(subject_id, team_id, False)
            db.session.commit()
            return '您已经同意小组选中您的课题，已拒绝其他申请'
        # 申请已经满了
        else:
            return '无法同意该申请，该课题已经全部选中'
    except Exception as err:
        logging.warning(err)
        return '地址不正确'


@bp.route('/select/refuse', methods=['POST'])
def refuse_select_mail():
    try:
        subject_id = request.args.get('subject_id')
        team_id = request.args.get('team_id')
        key2 = request.args.get('accessor')
        instructor = controller.subject_controller.query_instructor_by_subject_id(subject_id)
        # 如果accessor不正确
        if not check_password_hash(key2, instructor.password):
            return '错误的URL格式'
        controller.student_controller.update_apply_select(subject_id, team_id, False)
        return '您已经拒绝该小组选中您的课题'
    except Exception as err:
        logging.warning(err)
        return '地址不正确'
