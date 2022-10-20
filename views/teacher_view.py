from flask import Blueprint
from models import Instructor, ReleaseSubject
from common.ext import db
from flask import jsonify,request
import uuid

bp = Blueprint("teacher_view",__name__,url_prefix="/teacher")

#查找所有导师的信息
@bp.route("/list",methods = ['GET'])
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
            return  jsonify(code = 200,msg = "查找成功",data = teachers)
        else:
            return jsonify(code = 200,msg = "没有数据",data = teachers)
    except:
        return jsonify(code = 400,msg = "查找失败，遇到错误啦")


# 根据导师ID查找导师的信息
@bp.route("/id/<string:teacherID>", methods=['GET'])
def getTeacherById(teacherID):
    try:
        teacher = db.session.query(Instructor).filter_by(instructor_id = teacherID)[0]
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

#注册导师账号
@bp.route("/register",methods = ['POST'])
def teacherRegister():
    try:
        teacher_id = getId()
        teacher_name = request.form.get("name")
        teacher_password = request.form.get("password")
        teacher_phone = request.form.get("phone")
        teacher_email = request.form.get("email")
        teacher_description = request.form.get("description")
        teacher_gender = request.form.get("gender")
        teacher_birthday = request.form.get("birthday")#格式 xxxx-xx-xx
        teacher_title = request.form.get("title")
        teacher_dept = request.form.get("dept")
        teacher = Instructor(instructor_id = teacher_id,dept_id = teacher_dept, password = teacher_password,phone_number = teacher_phone,email = teacher_email \
                            ,description = teacher_description, gender = teacher_gender, birthday = teacher_birthday, instructor_name = teacher_name, \
                            title = teacher_title)

        db.session.add(teacher)
        db.session.commit()
        t = row2dict(teacher)
        return jsonify(code = 200,msg = "注册成功",data = t)
    except:
        return jsonify(code = 400,msg = "注册失败，请重试" )

#根据导师Id，修改导师信息
@bp.route("/update",methods = ['POST'])
def teacherUpdate():
    try:
        teacher_id = request.form.get("id")
        teacher = db.session.query(Instructor).filter_by(instructor_id = teacher_id)[0]
        teacher_name = request.form.get("name")
        if teacher_name is not None and teacher_name != teacher.instructor_name:
            teacher.instructor_name = teacher_name

        teacher_password = request.form.get("password")
        if teacher_password is not None and teacher_password != teacher.password:
            teacher.password = teacher_password

        teacher_phone = request.form.get("phone")
        if teacher_phone is not None and teacher_phone != teacher.phone_number:
            teacher.phone_number = teacher_phone

        teacher_email = request.form.get("email")
        if teacher_email is not None and teacher_email != teacher.email:
            teacher.email = teacher_email

        teacher_description = request.form.get("description")
        if teacher_description is not None and teacher_description != teacher.description:
            teacher.description = teacher_description

        teacher_gender = request.form.get("gender")
        if teacher_gender is not None and teacher_gender != teacher.gender:
            teacher.gender = teacher_gender

        teacher_birthday = request.form.get("birthday")#格式 xxxx-xx-xx
        if teacher_birthday is not None and teacher_birthday != teacher.birthday:
            teacher.birthday = teacher_birthday

        teacher_title = request.form.get("title")
        if teacher_title is not None and teacher_title != teacher.title:
            teacher.title = teacher_title

        teacher_dept = request.form.get("dept")
        if teacher_dept is not None and teacher_dept != teacher.dept_id:
            teacher.dept_id = teacher_dept

        db.session.commit()

        return jsonify(code = 200,msg = "信息修改成功")
    except:
        return jsonify(code = 400,msg = "修改失败，请重试" )


#查找该导师的所有课题信息
@bp.route("/subject/list/<string:teacherId>",methods = ['GET'])
def getSubjectList(teacherId):
    try:
        rs = db.session.query(ReleaseSubject).filter_by(instructor_id = teacherId).all()
        #print(rs)
        if rs is None:
            return jsonify(code = 200, msg = "该导师暂未发布题目")
        subjects = []
        for r in rs:
            sb = row2dict(r.subject)
            subjects.append(sb)

        return jsonify(code = 200 , msg = "查找成功！",data = subjects)
    except:
        return jsonify(code=400, msg="查找失败！")

#修改课题

# 数据库类对象转为字典
def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d

#获取ID，使用UUID
def getId():
    return uuid.uuid4().hex[:16]