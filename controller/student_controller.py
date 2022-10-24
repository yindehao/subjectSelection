# _*_ coding: utf-8 _*_
"""
Time:     2022/10/22 15:15
Author:   Yin Dehao
Version:  V 1.0
File:     StudentController
"""
import time

from sqlalchemy import func

from common.ext import db
from common.row2dict import row2dict
from controller.subject_controller import query_subject_by_id
from models import Student, Dept, t_wish_list, Subject, Instructor, ReleaseSubject, Team


# 根据学生姓名模糊查找学生
def query_student_by_name(student_name):
    student = db.session.query(Student).filter(Student.student_name.like(f'%{student_name}%')).all()
    return student


# 根据ID查找学生
def query_student_by_id(student_id):
    student = db.session.query(Student).filter_by(student_id=student_id).first()
    return student


# 根据team_id查找同一组的学生
def query_student_by_team_id(team_id):
    students = db.session.query(Student).filter_by(team_id=team_id).all()
    return students


'''
小组的创建、加入、退出、修改、删除
'''


# 创建小组
def create_team_by_leader(leader_id, team_name):
    team = Team()
    team.leader_id = leader_id
    team.team_name = team_name
    team.team_id = int(leader_id[2:])
    team.subject_id = None
    team.version = 1
    team.subject_id = None
    db.session.add(team)
    return team


# 加入小组
def join_team_by_team_id(student_id, team_id):
    student = query_student_by_id(student_id)
    student.team_id = team_id
    db.session.commit()
    return student


# 修改小组名称
def update_team_name(team_id, team_name):
    team = query_team_by_id(team_id)
    team.team_name = team_name
    db.session.commit()
    return team


# 退出小组, 如果是队长退出了，那么小队会解散
def withdraw_team_by_student_id(student_id):
    student = query_student_by_id(student_id)
    if student.team_id:
        team = query_team_by_id(student.team_id)
        if team.leader_id == student.student_id:
            delete_team_by_team_id(team.team_id)
        else:
            student.team_id = None
            db.session.commit()
    return student


# 删除小组
def delete_team_by_team_id(team_id):
    team = query_team_by_id(team_id)
    students = query_student_by_team_id(team_id)
    # 清空wish_list
    delete_wish_list_all(team_id)
    # todo 清空选课申请
    for student in students:
        student.team_id = None
    db.session.delete(team)
    db.session.commit()
    return True


# 根据team_id获取team
def query_team_by_id(team_id):
    team = db.session.query(Team).filter_by(team_id=team_id).first()
    return team


# 获取小组的全部信息，包括组员姓名学号、组长姓名学号
def query_team_full_by_id(team_id):
    team = query_team_by_id(team_id)
    # 根据team_id查找同一组的学生
    students = query_student_by_team_id(team_id)
    team_leader = query_student_by_id(team.leader_id)
    data = dict()
    data['team_id'] = row2dict(team)
    if team.subject_id:
        subject = query_subject_by_id(team.subject_id)
        data['team_id']['subject_name'] = subject.subject_name
    data['teammates'] = list()
    data['team_leader'] = team_leader.student_id
    # 将所有学生信息传到JSON中
    for stu2 in students:
        stu2_info = dict()
        stu2_info['student_id'] = stu2.student_id
        stu2_info['student_name'] = stu2.student_name
        data['teammates'].append(stu2_info)
    return data


def query_team_count(team_id):
    count = db.session.query(func.count(Student.student_id)).join(Team, Team.team_id == Student.team_id). \
        filter(Student.team_id == team_id).first()[0]
    return count


# 根据dept_id查找院系
def query_dept_by_id(dept_id):
    dept = db.session.query(Dept).filter_by(dept_id=dept_id).first()
    return dept


# 获取愿望单中的课题信息，和加入愿望单的时间
def query_wish_list_by_team_id(team_id):
    sql = 'select s.subject_id,s.subject_name, s.language,' \
          'i.instructor_name, s.origin, s.min_person,s.max_person, s.max_group, wish_list.join_time ' \
          'from wish_list join subject s on s.subject_id = wish_list.subject_id ' \
          'join release_subject rs on s.subject_id = rs.subject_id ' \
          'join instructor i on i.instructor_id = rs.instructor_id ' \
          'where wish_list.team_id = :team_id'
    wish_list = db.session.execute(sql, {'team_id': team_id})
    return wish_list


# 添加愿望单
def add_2_wish_list(team_id, subject_id):
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql = 'insert into wish_list(subject_id, team_id, join_time) ' \
          'values(:subject_id, :team_id, :join_time)'
    db.session.execute(sql, {'subject_id': subject_id, 'team_id': team_id, 'join_time': now})
    db.session.commit()


def delete_wish_list(team_id, subject_id):
    sql = 'delete from wish_list ' \
          'where subject_id = :subject_id  and team_id = :team_id;'
    db.session.execute(sql, {'subject_id': subject_id, 'team_id': team_id})
    db.session.commit()


def query_wish_by_id(team_id, subject_id):
    sql = 'select s.subject_id,s.subject_name, s.language,' \
          'i.instructor_name, s.origin, s.min_person,s.max_person, s.max_group, wish_list.join_time ' \
          'from wish_list join subject s on s.subject_id = wish_list.subject_id ' \
          'join release_subject rs on s.subject_id = rs.subject_id ' \
          'join instructor i on i.instructor_id = rs.instructor_id ' \
          'where wish_list.subject_id = :subject_id and wish_list.team_id = :team_id'
    wish = db.session.execute(sql, {'subject_id': subject_id, 'team_id': team_id}).first()
    return wish

# 删除小队的所有愿望
def delete_wish_list_all(team_id):
    sql = 'delete from wish_list ' \
          'where team_id = :team_id;'
    db.session.execute(sql, {'team_id': team_id})
    db.session.commit()
    return True
