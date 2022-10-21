from flask import Blueprint
from flask import jsonify
from models import Student
from common.ext import db
bp = Blueprint("studentController",__name__,url_prefix="/student")

##student接口，所有api都需要加上前缀 "/student"

#查找所有student信息
@bp.route("/list",methods = ['GET'])
def getStudentList():
    try:
        studentList = db.session.query(Student).all()
        list = []
        if studentList is not None:
            for s in studentList:
                student = {}
                student["id"] = s.student_id
                student["team_id"] = s.team_id
                student["dept_id"] = s.dept_id
                student["phone_number"] = s.phone_number
                student["email"] = s.email
                student["description"] = s.description
                if(s.gender == 1):
                    student["gender"] = "男"
                else:
                    student["gender"] = "女"
                student["birthday"] = s.birthday
                student["name"] = s.student_name
                student["type"] = s.student_type
                student["class"] = s.student_class
                list.append(student)
            return jsonify(code = 200,msg = "查找成功",data = list)
        else:
            return jsonify(code=200, msg="没有数据", data = list)
    except:
        return jsonify(code = 400,msg = "查询失败")


#根据ID查找学生
@bp.route("/id/<string:studentId>",methods = ['GET'])
def getStudentByID(studentId):
    try:
        s = db.session.query(Student).filter_by(student_id = studentId)[0]
        list = []
        if s is not None:
            student = {}
            student["id"] = s.student_id
            student["team_id"] = s.team_id
            student["dept_id"] = s.dept_id
            student["phone_number"] = s.phone_number
            student["email"] = s.email
            student["description"] = s.description
            if(s.gender == 1):
                student["gender"] = "男"
            else:
                student["gender"] = "女"
            student["birthday"] = s.birthday
            student["name"] = s.student_name
            student["type"] = s.student_type
            student["class"] = s.student_class
            list.append(student)
            return jsonify(code = 200,msg = "查找成功",data = list)
        else:
            return jsonify(code=200, msg="没有数据", data = list)
    except:
        return jsonify(code = 400,msg = "查询失败")



