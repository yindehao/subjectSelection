# _*_ coding: utf-8 _*_
"""
Time:     2022/10/26 11:01
Author:   Yin Dehao
Version:  V 1.0
File:     teacher_controller
"""
from common.ext import db
from common.utils2 import row2dict
from controller.student_controller import query_dept_by_id
from models import Instructor


def get_gender(gender):
    return "男" if gender else "女"


def get_dept_name_by_id(dept_id):
    dept = query_dept_by_id(dept_id)
    return dept.dept_name


def instor_2_instructor(instructor):
    data = row2dict(instructor)
    data['gender'] = get_gender(instructor.gender)
    data['dept_name'] = get_dept_name_by_id(instructor.dept_id)
    return data


def query_instructor_by_id(instructor_id):
    instructor = db.session.query(Instructor).filter(Instructor.instructor_id == instructor_id).first()
    return instructor
