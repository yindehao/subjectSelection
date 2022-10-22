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
from common.row2dict import row2dict
from models import Instructor, Subject, ReleaseSubject

bp = Blueprint("svbp", __name__, url_prefix='/subjects')


# 筛选条件课题
# url格式: /subjects?params1=value1&params2=value2
@bp.route('', methods=['GET'])
def get_subjects_by_args():
    # 获得筛选条件
    # 导师姓名支持多选
    instructor_names = request.args.getlist('instructor_name')
    # 开发语言支持多选
    language = request.args.get('language')
    # 题目来源
    origins = request.args.getlist('origin')
    # 默认人数为1-4人
    min_person = int(request.args.get('min_person', 1))
    max_person = int(request.args.get('max_person', 4))
    # 分页 第几页page_index 页面大小page_size
    page_index = int(request.args.get('page_index', 1))
    page_size = int(request.args.get('page_size', 20))
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
    return jsonify(data=data, code='200')


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
        'code': '200',
        'data': data,
    }
    return jsonify(res)


# 根据subject_id查询课题所有信息
# url格式：http://127.0.0.1:5000/subjects/subject_id
@bp.route('/<int:subject_id>', methods=['GET'])
def get_subject_by_id(subject_id):
    try:
        subject = db.session.query(Subject).filter(Subject.subject_id == subject_id).first()
        data = row2dict(subject)
        print(data)
        instructor_name = db.session.query(Instructor.instructor_name). \
            join(ReleaseSubject, ReleaseSubject.instructor_id == Instructor.instructor_id). \
            join(Subject, ReleaseSubject.subject_id == Subject.subject_id). \
            filter(Subject.subject_id == subject_id).first()[0]

        data['instructor_name'] = instructor_name
        print(data)
        return jsonify(code=200, data=data)
    except TypeError as err:
        print(TypeError)
        return jsonify(code=400, msg='Type Error')


@bp.route('/count', methods=['GET'])
def get_subject_count():
    count = db.session.query(func.count(Subject.subject_id)).first()[0]
    return jsonify(count)
