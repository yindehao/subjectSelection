# _*_ coding: utf-8 _*_
"""
Time:     2022/10/22 15:15
Author:   Yin Dehao
Version:  V 1.0
File:     StudentController
"""
from common.ext import db
from common.row2dict import row2dict
from models import Student, Dept, t_wish_list, Subject, Instructor, ReleaseSubject


# 根据学生姓名模糊查找学生
def query_student_by_name(student_name):
    student = db.session.query(Student).filter(Student.student_name.like(f'%{student_name}%')).first()
    return student


# 根据ID查找学生
def query_student_by_id(student_id):
    student = db.session.query(Student).filter_by(student_id=student_id).first()
    return student


def query_dept_by_id(dept_id):
    dept = db.session.query(Dept).filter_by(dept_id=dept_id).first()
    return dept


# 获取愿望单中的课题信息，和加入愿望单的时间
def query_wish_list_by_team_id(team_id):
    wish_list = not db.session.query(t_wish_list.join_time, Subject.subject_id, Subject.subject_name, Subject.language,
                                     Instructor.instructor_name, Subject.origin, Subject.min_person,
                                     Subject.max_person, Subject.max_group).\
        join(Subject, Subject.subject_id == t_wish_list.subject_id). \
        join(ReleaseSubject, ReleaseSubject.subject_id == Subject.subject_id). \
        join(Instructor, Instructor.instructor_id == ReleaseSubject.subject_id). \
        filter(t_wish_list.team_id == team_id).all()
    return wish_list
