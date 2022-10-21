from flask import Flask, render_template, session, url_for, redirect, request
from werkzeug.security import check_password_hash, generate_password_hash

from common import config
from common.ext import db, cors
from common.forms import LoginForm
from models import Student, Instructor, Subject, ReleaseSubject
from views import student_bp
from views import instructor_bp


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
cors.init_app(app)
# 注册路由视图
app.register_blueprint(student_bp)
app.register_blueprint(instructor_bp)


# 测试数据库连接
@app.route('/test_connection')
def test_connection():
    # 测试数据库连接，查询当前时间
    now = db.session.execute('SELECT SYSDATE()').first()[0]
    print(f'当前时间为 {now}')
    return f'当前时间为 {now}'


# 运行后，如果当前用户未登录，重定向到登录界面；如果已经登录，重定向到导师/用户主页界面
@app.route('/')
def index():
    # 如果已经登录了学生账号,跳转到学生主页界面
    if 'student_id' in session:
        return redirect(url_for("sbp.index"))
    # 如果登录了导师账号,跳转到导师主页界面
    elif 'instructor_id' in session:
        return redirect(url_for("ibp.index"))
    # 登录界面
    else:
        return redirect(url_for('login'))


# 筛选条件课题
# url格式: /subjects/?params1=value1&params2=value2
@app.route('/subjects', methods=['GET'])
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
        # data[subject.subject_id] = {
        #     'subject_id': subject[0],
        #     'subject_name': subject[1],
        #     'language': subject[2],
        #     'instructor_name': subject[3],
        #     'origin':subject
        # }

    response = {
        'data': data,
        'code': '200'
    }
    return response


if __name__ == '__main__':
    app.run()
