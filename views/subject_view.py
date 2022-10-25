# _*_ coding: utf-8 _*_
"""
Time:     2022/10/21 20:14
Author:   Yin Dehao
Version:  V 1.0
File:     subject_view
"""

from flask import Blueprint, request, jsonify
from sqlalchemy import func

from common.ext import db
from common.utils2 import row2dict
from controller.student_controller import get_accept_apply_select_count
from controller.subject_controller import query_subject_by_id, query_instructor_name_by_subject_id, \
    query_subject_by_name
from models import Instructor, Subject, ReleaseSubject

bp = Blueprint("svbp", __name__, url_prefix='/subjects')


# 根据请求的不定参数，生成过滤器列表
def get_filter_list_by_args(request2):
    # 获得筛选条件
    # 导师姓名支持多选
    instructor_names = request2.args.getlist('instructor_name')
    # 开发语言支持多选
    language = request2.args.get('language')
    # 题目来源
    origins = request2.args.getlist('origin')
    # 默认人数为1-4人
    min_person = int(request2.args.get('min_person', 1))
    max_person = int(request2.args.get('max_person', 4))

    filter_list = []
    if instructor_names:
        filter_list.append(Instructor.instructor_name.in_(instructor_names))
    if language:
        filter_list.append(Subject.language.like(f'%{language}%'))
    if origins:
        filter_list.append(Subject.origin.in_(origins))

    # 人数限制
    filter_list.append(Subject.max_person <= max_person)
    filter_list.append(Subject.min_person >= min_person)
    return filter_list


# 筛选条件课题
# url格式: /subjects?params1=value1&params2=value2
@bp.route('', methods=['GET'])
def get_subjects_by_args():
    try:
        filter_list = get_filter_list_by_args(request)
        # 分页 第几页page_index 页面大小page_size
        page_index = int(request.args.get('page_index', 1))
        page_size = int(request.args.get('page_size', 20))

        filter_query = db.session.query(Subject.subject_id, Subject.subject_name, Subject.language,
                                        Instructor.instructor_name, Subject.origin, Subject.min_person,
                                        Subject.max_person, Subject.max_group). \
            outerjoin(ReleaseSubject, ReleaseSubject.subject_id == Subject.subject_id). \
            outerjoin(Instructor, ReleaseSubject.instructor_id == Instructor.instructor_id). \
            filter(*filter_list).limit(page_size).offset((page_index - 1) * page_size)
        print(filter_query)
        subjects = filter_query.all()
        print(subjects)
        data = dict()
        data_keys = ['subject_id', 'subject_name', 'language', 'instructor_name',
                     'origin', 'min_person', 'max_person', 'max_group']
        for subject in subjects:
            data[subject.subject_id] = dict()
            for key_index in range(len(data_keys) - 1):
                data[subject.subject_id][data_keys[key_index]] = subject[key_index]
        return jsonify(data=data, code=200)
    except TypeError as err:
        return jsonify(code=400, msg='找不到给定参数的课题')


# 获取所有筛选条件
@bp.route('/items', methods=['GET'])
def get_distinct_items():
    # 获取筛选项
    instructor_names = db.session.query(Instructor.instructor_name).distinct().all()
    origins = db.session.query(Subject.origin).distinct().all()

    languages = ['C', 'C++', 'C#', 'Python', 'Java', 'Go', 'Rust', 'SQL', 'Swift', 'R', 'Kotlin', 'Matlab']
    max_person = db.session.query(func.max(Subject.max_person)).first()
    min_person = db.session.query(func.min(Subject.min_person)).first()
    data = dict()

    data['instructor_names'] = [instructor_name[0] for instructor_name in instructor_names]
    data['origin'] = [origin[0] for origin in origins]
    data['languages'] = languages
    data['min_person'] = min_person[0]
    data['max_person'] = max_person[0]
    res = {
        'code': 200,
        'data': data,
    }
    return jsonify(res)


# 根据subject_id查询课题所有信息
# url格式：http://127.0.0.1:5000/subjects/subject_id
@bp.route('/<int:subject_id>', methods=['GET'])
def get_subject_by_id(subject_id):
    try:
        subject = query_subject_by_id(subject_id)
        data = row2dict(subject)
        instructor_name = query_instructor_name_by_subject_id(subject_id)
        data['instructor_name'] = instructor_name
        print(data)
        return jsonify(code=200, data=data)
    except TypeError as err:
        print(TypeError)
        return jsonify(code=400, msg='Type Error')


# 获取所有课题数目
@bp.route('/count', methods=['GET'])
def get_subject_count():
    try:
        filter_list = get_filter_list_by_args(request)
        count = db.session.query(func.count(Subject.subject_id)). \
            outerjoin(ReleaseSubject, ReleaseSubject.subject_id == Subject.subject_id). \
            outerjoin(Instructor, ReleaseSubject.instructor_id == Instructor.instructor_id). \
            filter(*filter_list).first()[0]
        return jsonify(code=200, data=count, msg=f'找到指定条件的课题{count}个')
    except RuntimeError as err:
        return jsonify(code=400, data=0, msg=f'找不到指定条件的课题')


# 根据课题标题搜索课题 ?title=<subject_name>
@bp.route('/search', methods=['GET'])
def search_subject():
    try:
        subject_name = request.args.get('title')
        subjects = query_subject_by_name(subject_name)
        data = dict()
        for subject in subjects:
            data[subject.subject_id] = row2dict(subject)
            data[subject.subject_id]['instructor_name'] = query_instructor_name_by_subject_id(subject.subject_id)
        return jsonify(code=200, data=data, msg='成功找到课题')
    except Exception as err:
        print(err)
        return jsonify(code=400, data=dict(), msg='找不到课题')


#  查看选中某个课题的人数
@bp.route('/count/<subject_id>')
def subject_selected_count(subject_id):
    count = get_accept_apply_select_count(subject_id=subject_id)
    return jsonify(code=200, data={'count': count}, msg=f'当前已经有{count}个小组选中该课题')
