import logging

from flask import Blueprint, session
from werkzeug.security import check_password_hash, generate_password_hash

from common.utils2 import get_local_time
from controller.student_controller import query_apply_select_by_team, query_apply_select, query_apply_select_by_subject, \
    query_dept_by_id, delete_wish_list_by_subject_id
from controller.teacher_controller import get_dept_name_by_id, get_gender, instor_2_instructor, query_instructor_by_id
from models import Instructor, ReleaseSubject, Subject, Team
from common.ext import db
from flask import jsonify, request
import uuid
import time
import utils

bp = Blueprint("teacher_view", __name__, url_prefix="/teacher")


@bp.route("/login", methods=['POST'])
def login():
    form = request.json
    instructor_id = form['username']
    password = form['password']
    try:
        instructor = db.session.query(Instructor).filter_by(instructor_id=instructor_id).first()
        # 如果密码和加密后的密码匹配，则返回登录信息
        if instructor and check_password_hash(instructor.password, password):
            data = instor_2_instructor(instructor)
            session['instructor_id'] = instructor_id
            return jsonify(code=200, data=data, msg='学工号和密码匹配')
        # 如果是明文导入的密码，更改为哈希后的密码
        elif instructor and instructor.password == password:
            instructor.password = generate_password_hash(password)
            db.session.commit()
            data = instor_2_instructor(instructor)
            session['instructor_id'] = instructor_id
            return jsonify(code=200, data=data, msg='学号和密码匹配')
        else:
            return jsonify(code=400, msg='学号或者密码错误！')
    # 该学号不存在
    except Exception as err:
        logging.warning(err)
        return jsonify(code=400, msg=f'学工号 {instructor_id} 不存在系统中')


# 查找所有导师的信息
@bp.route("/list", methods=['GET'])
def getTeacherList():
    try:
        teacherList = db.session.query(Instructor).all()
        teachers = []
        for teacher in teacherList:
            t = instor_2_instructor(teacher)
            logging.info(t)
            teachers.append(t)
        if teachers is not None:
            return jsonify(code=200, msg="查找成功", data=teachers)
        else:
            return jsonify(code=200, msg="没有数据", data=teachers)
    except Exception as err:
        logging.error(err)
        return jsonify(code=400, msg="查找失败，遇到错误啦")


# 根据导师ID查找导师的信息
@bp.route("/id/<string:teacherID>", methods=['GET'])
def getTeacherById(teacherID):
    try:
        teacher = db.session.query(Instructor).filter_by(instructor_id=teacherID)[0]
        t = instor_2_instructor(teacher)
        if teacher:
            return jsonify(code=200, msg="查找成功", data=t)
        else:
            return jsonify(code=200, msg="没有数据", data=t)
    except Exception as err:
        logging.error(err)
        return jsonify(code=400, msg="查找失败，遇到错误啦")


# 注册导师账号
@bp.route("/register", methods=['POST'])
def teacherRegister():
    try:
        form = request.form
        teacher_id = getId()
        teacher_name = form.get("name")
        teacher_password = form.get("password")
        teacher_phone = form.get("phone")
        teacher_email = form.get("email")
        teacher_description = form.get("description")
        teacher_gender = form.get("gender")
        teacher_birthday = form.get("birthday")  # 格式 xxxx-xx-xx
        teacher_title = form.get("title")
        teacher_dept = form.get("dept")
        teacher = Instructor(instructor_id=teacher_id, dept_id=teacher_dept, password=teacher_password,
                             phone_number=teacher_phone, email=teacher_email,
                             description=teacher_description, gender=teacher_gender, birthday=teacher_birthday,
                             instructor_name=teacher_name,
                             title=teacher_title)

        db.session.add(teacher)
        db.session.commit()
        t = row2dict(teacher)
        return jsonify(code=200, msg="注册成功", data=t)
    except Exception as err:
        logging.error(err)
        return jsonify(code=400, msg="注册失败，请重试")


# 根据导师Id，修改导师信息
@bp.route("/update", methods=['POST'])
def teacherUpdate():
    try:
        form = request.json
        instructor_id = form['username']
        instructor = query_instructor_by_id(instructor_id)
        # 可能修改的字段：手机号，邮箱，生日，自我介绍
        instructor.phone_number = form['TELE']
        instructor.email = form['Email']
        instructor.birthday = form['birthday'][0:10]
        instructor.description = form['description']
        db.session.commit()
        return jsonify(code=200, data=instor_2_instructor(instructor), msg="信息修改成功")
    except Exception as err:
        logging.error(err)
        return jsonify(code=400, msg="修改失败，请重试")


# 查找该导师的所有课题信息
@bp.route("/subject/list/<string:teacherId>", methods=['GET'])
def getSubjectList(teacherId):
    try:
        rs = db.session.query(ReleaseSubject).filter_by(instructor_id=teacherId).all()
        # print(rs)
        if rs is None:
            return jsonify(code=200, msg="该导师暂未发布题目")
        subjects = []
        for r in rs:
            sb = row2dict(r.subject)
            subjects.append(sb)

        return jsonify(code=200, msg="查找成功！", data=subjects)
    except Exception as err:
        logging.error(err)
        return jsonify(code=400, msg="查找失败！")


# 发布课题
@bp.route("/subject/post", methods=['POST'])
def postSubject():
    try:
        form = request.json
        t_id = form.get("id")  # teacher id
        s_name = form.get("name")
        s_description = form.get("description")
        s_language = form.get("language")
        s_platform = form.get("platform")
        s_min_person = form.get("min_person")
        s_max_person = form.get("max_person")
        s_innovation = form.get("innovation")
        s_max_group = form.get("max_group")
        s_origin = form.get("origin")
        creatTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 2020-06-26 22:00:24
        s_id = utils.IdWorker(1, 2, 20).get_id()  # ID雪花算法

        subject = Subject(subject_id=s_id, subject_name=s_name, description=s_description, language=s_language,
                          platform=s_platform, min_person=int(s_min_person), max_person=int(s_max_person),
                          innovation=s_innovation, max_group=int(s_max_group), origin=s_origin,
                          created_time=creatTime, last_modified_time=creatTime, version=1)
        rs = ReleaseSubject(instructor_id=t_id, subject_id=subject.subject_id, released=1, version=subject.version)
        db.session.add(subject)
        db.session.add(rs)
        db.session.commit()
        return jsonify(code=200, msg="课题增加成功", data=row2dict(subject))
    except Exception as err:
        logging.error(err)
        jsonify(code=400, msg="课题增加失败，请重试")


# 修改课题
@bp.route("/subject/upgrade", methods=['POST'])
def upgradeSubject():
    try:
        form = request.json
        subject_id = form.get("id")  # subject id
        s = db.session.query(Subject).filter_by(subject_id=subject_id).first()
        s.subject_name = form.get("name",s.subject_name)
        s.description = form.get("description",s.description)
        s.language = form.get("language",s.language)
        s.platform = form.get("platform",s.platform)
        s.min_person = form.get("min_person",s.min_person)
        s.max_person = form.get("max_person",s.max_person)
        s.max_group = form.get("max_group",s.max_group)
        s.origin = form.get("origin",s.origin)
        s.innovation = form.get("innovation",s.innovation)
        s.last_modified_time = get_local_time()
        s.version = s.version + 1
        db.session.add(s)
        db.session.commit()
        return jsonify(code=200, msg="课题修改成功", data=row2dict(s))
    except Exception as err:
        logging.error(err)
        jsonify(code=400, msg="课题修改失败，请重试")


# 删除课题
@bp.route("/subject/delete/<int:subjectId>", methods=['GET'])
def deleteSubject(subjectId):
    try:
        if subjectId == "":
            return jsonify(code=200, msg="没有该课题,删除失败")
        t = db.session.query(Team).filter_by(subject_id=subjectId).all()
        print(t)
        if len(t) > 0:
            return jsonify(code=200, msg="该课题已经被选择，无法删除")

        s = db.session.query(Subject).filter_by(subject_id=subjectId)[0]
        # print(s)
        rs = db.session.query(ReleaseSubject).filter_by(subject_id=subjectId)[0]
        delete_wish_list_by_subject_id(subjectId)
        if rs is not None:
            db.session.delete(rs)
            db.session.commit()
        # time.sleep(0.5)

        if s is not None:
            db.session.delete(s)
            db.session.commit()
        return jsonify(code=200, msg="课题删除成功")
    except Exception as err:
        logging.error(err)
        return jsonify(code=400, msg="删除失败请重试")


# 数据库类对象转为字典
def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d


# 获取ID，使用UUID
def getId():
    return uuid.uuid4().hex[:16]


# 导师查看选题结果
@bp.route('/subject/<subject_id>', methods=['GET'])
def selected_subject(subject_id):
    try:
        applies = query_apply_select_by_subject(subject_id)
        data = list()
        for apply in applies:
            data.append(row2dict(apply))
        return jsonify(code=200, data=data, msg='成功获得选题申请')
    except Exception as err:
        logging.warning(err)
        return jsonify(code=400, data=dict(), msg='无法获取选中课题信息')
