from flask import Blueprint
from models import Instructor, ReleaseSubject, Subject, Team
from common.ext import db
from flask import jsonify, request
import uuid
import time
import utils

bp = Blueprint("teacher_view", __name__, url_prefix="/teacher")


# 查找所有导师的信息
@bp.route("/list", methods=['GET'])
def getTeacherList():
    try:
        teacherList = db.session.query(Instructor).all()
        teachers = []
        for teacher in teacherList:
            print(teacher)
            if teacher.gender == 1:
                teacher.gender = "男"
            else:
                teacher.gender = "女"
            t = row2dict(teacher)
            teachers.append(t)
        print(teachers)
        if teachers is not None:
            return jsonify(code=200, msg="查找成功", data=teachers)
        else:
            return jsonify(code=200, msg="没有数据", data=teachers)
    except:
        return jsonify(code=400, msg="查找失败，遇到错误啦")


# 根据导师ID查找导师的信息
@bp.route("/id/<string:teacherID>", methods=['GET'])
def getTeacherById(teacherID):
    try:
        teacher = db.session.query(Instructor).filter_by(instructor_id=teacherID)[0]
        if teacher.gender == 1:
            teacher.gender = "男"
        else:
            teacher.gender = "女"
        t = row2dict(teacher)
        if teacher is not None:
            return jsonify(code=200, msg="查找成功", data=t)
        else:
            return jsonify(code=200, msg="没有数据", data=t)
    except:
        return jsonify(code=400, msg="查找失败，遇到错误啦")


# 注册导师账号
@bp.route("/register", methods=['POST'])
def teacherRegister():
    try:
        teacher_id = getId()
        teacher_name = request.form.get("name")
        teacher_password = request.form.get("password")
        teacher_phone = request.form.get("phone")
        teacher_email = request.form.get("email")
        teacher_description = request.form.get("description")
        teacher_gender = request.form.get("gender")
        teacher_birthday = request.form.get("birthday")  # 格式 xxxx-xx-xx
        teacher_title = request.form.get("title")
        teacher_dept = request.form.get("dept")
        teacher = Instructor(instructor_id=teacher_id, dept_id=teacher_dept, password=teacher_password,
                             phone_number=teacher_phone, email=teacher_email \
                             , description=teacher_description, gender=teacher_gender, birthday=teacher_birthday,
                             instructor_name=teacher_name, \
                             title=teacher_title)

        db.session.add(teacher)
        db.session.commit()
        t = row2dict(teacher)
        return jsonify(code=200, msg="注册成功", data=t)
    except:
        return jsonify(code=400, msg="注册失败，请重试")


# 根据导师Id，修改导师信息
@bp.route("/update", methods=['POST'])
def teacherUpdate():
    try:
        teacher_id = request.form.get("id")
        teacher = db.session.query(Instructor).filter_by(instructor_id=teacher_id)[0]
        teacher_name = request.form.get("name")
        if teacher_name != "" and teacher_name != teacher.instructor_name:
            teacher.instructor_name = teacher_name

        teacher_password = request.form.get("password")
        if teacher_password != "" and teacher_password != teacher.password:
            teacher.password = teacher_password

        teacher_phone = request.form.get("phone")
        if teacher_phone != "" and teacher_phone != teacher.phone_number:
            teacher.phone_number = teacher_phone

        teacher_email = request.form.get("email")
        if teacher_email != "" and teacher_email != teacher.email:
            teacher.email = teacher_email

        teacher_description = request.form.get("description")
        if teacher_description != "" and teacher_description != teacher.description:
            teacher.description = teacher_description

        teacher_gender = request.form.get("gender")
        if teacher_gender != "" and teacher_gender != teacher.gender:
            teacher.gender = teacher_gender

        teacher_birthday = request.form.get("birthday")  # 格式 xxxx-xx-xx
        if teacher_birthday != "" and teacher_birthday != teacher.birthday:
            teacher.birthday = teacher_birthday

        teacher_title = request.form.get("title")
        if teacher_title != "" and teacher_title != teacher.title:
            teacher.title = teacher_title

        teacher_dept = request.form.get("dept")
        if teacher_dept != "" and teacher_dept != teacher.dept_id:
            teacher.dept_id = teacher_dept

        db.session.commit()

        return jsonify(code=200, msg="信息修改成功")
    except:
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
    except:
        return jsonify(code=400, msg="查找失败！")


# 发布课题
@bp.route("/subject/post", methods=['POST'])
def postSubject():
    try:
        t_id = request.form.get("id")  # teacher id
        s_name = request.form.get("name")
        s_description = request.form.get("description")
        s_language = request.form.get("language")
        s_platform = request.form.get("platform")
        s_min_person = request.form.get("min_person")
        s_max_person = request.form.get("max_person")
        s_innovation = request.form.get("innovation")
        s_max_group = request.form.get("max_group")
        s_origin = request.form.get("origin")
        creatTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 2020-06-26 22:00:24
        s_id = utils.IdWorker(1, 2, 0).get_id()  # ID雪花算法

        subject = Subject(subject_id=s_id, subject_name=s_name, description=s_description, language=s_language, \
                          platform=s_platform, min_person=s_min_person, max_person=s_max_person,
                          innovation=s_innovation, \
                          max_group=s_max_group, origin=s_origin, created_time=creatTime, last_modified_time=creatTime,
                          version=1)
        rs = ReleaseSubject(instructor_id=t_id, subject_id=subject.subject_id, released=1, version=subject.version)

        db.session.add(subject)
        db.session.add(rs)
        db.session.commit()
        return jsonify(code=200, msg="课题增加成功", data=row2dict(subject))
    except:
        jsonify(code=400, msg="课题增加失败，请重试")


# 修改课题
@bp.route("/subject/upgrade", methods=['POST'])
def upgradeSubject():
    try:
        s_id = request.form.get("id")  # subject id
        s = db.session.query(Subject).filter_by(subject_id=s_id)[0]
        s_name = request.form.get("name")
        if s_name != "" and s.subject_name != s_name:
            s.subject_name = s_name
        s_description = request.form.get("description")
        if s_description != "" and s.description != s_description:
            s.description = s_description
        s_language = request.form.get("language")
        if s_language != "" and s.language != s_language:
            s.language = s_language
        s_platform = request.form.get("platform")
        if s_platform != "" and s.platform != s_platform:
            s.platform = s_platform
        s_min_person = request.form.get("min_person")
        if s_min_person != "" and s.min_person != s_min_person:
            s.min_person = s_min_person
        s_max_person = request.form.get("max_person")
        if s_max_person != "" and s.max_person != s_max_person:
            s.max_person = s_max_person
        s_innovation = request.form.get("innovation")
        if s_innovation != "" and s.innovation != s_innovation:
            s.innovation = s_innovation
        s_max_group = request.form.get("max_group")
        if s_max_group != "" and s.max_group != s_max_group:
            s.max_group = s_max_group
        s_origin = request.form.get("origin")
        if s_origin != "" and s.origin != s_origin:
            s.origin = s_origin
        mTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 2020-06-26 22:00:24
        s.last_modified_time = mTime
        s.version = s.version + 1
        db.session.add(s)
        db.session.commit()
        return jsonify(code=200, msg="课题修改成功", data=row2dict(s))
    except:
        jsonify(code=400, msg="课题修改失败，请重试")


# 删除课题
@bp.route("subject/delete/<int:subjectId>", methods=['GET'])
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
        if rs is not None:
            db.session.delete(rs)
            db.session.commit()
        # time.sleep(0.5)
        if s is not None:
            db.session.delete(s)
            db.session.commit()
        return jsonify(code=200, msg="课题删除成功")
    except:
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
