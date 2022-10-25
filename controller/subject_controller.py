# _*_ coding: utf-8 _*_
"""
Time:     2022/10/23 14:10
Author:   Yin Dehao
Version:  V 1.0
File:     subject_controller
"""
from common.ext import db
from models import Subject, Instructor, ReleaseSubject


# 根据ID查找课题
def query_subject_by_id(subject_id):
    subject = db.session.query(Subject).filter(Subject.subject_id == subject_id).first()
    return subject


# 根据标题查找课题，模糊查找，返回列表
def query_subject_by_name(subject_name):
    subjects = db.session.query(Subject).filter(Subject.subject_name.like(f'%{subject_name}%')).all()
    return subjects


# 根据课题ID查找导师姓名
def query_instructor_name_by_subject_id(subject_id):
    instructor_name = db.session.query(Instructor.instructor_name). \
        join(ReleaseSubject, ReleaseSubject.instructor_id == Instructor.instructor_id). \
        join(Subject, ReleaseSubject.subject_id == Subject.subject_id). \
        filter(Subject.subject_id == subject_id).first()[0]
    return instructor_name


# 根据课题ID查找导师信息
def query_instructor_by_subject_id(subject_id):
    instructor = db.session.query(Instructor). \
        join(ReleaseSubject, ReleaseSubject.instructor_id == Instructor.instructor_id). \
        join(Subject, ReleaseSubject.subject_id == Subject.subject_id). \
        filter(Subject.subject_id == subject_id).first()
    return instructor


