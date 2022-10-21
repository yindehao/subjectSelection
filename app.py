from flask import Flask, render_template, session, url_for, redirect, request
from werkzeug.security import check_password_hash, generate_password_hash

from common import config
from common.ext import db
from common.forms import LoginForm
from models import Student, Instructor
from views import student_bp
from views import instructor_bp
from views import student_index
from views import instructor_index
from controller import studentController
from views import teacher_view

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            user_id = form.username.data
            password = form.password.data
            # 学生登录
            if user_id.startswith('SA'):
                student_id = user_id
                student = db.session.query(Student).filter_by(student_id=student_id)[0]
                if student and check_password_hash(student.password, password):
                    session['student_id'] = student.student_id
                    # todo 设置会话过期时间
                    return redirect(url_for("sbp.index"))
                elif student and student.password == password:
                    # 如果用户密码是密文存储，则将密码更改为哈希后的密码
                    student.password = generate_password_hash(password)
                    db.session.commit()
                    session['student_id'] = student_id
                    return redirect(url_for("sbp.index"))
                else:
                    # todo 调用前端接口弹出提示
                    print("学工号或密码错误")
                    return redirect(url_for("login"))

            # 导师登录
            elif user_id.startswith('TA'):
                instructor_id = user_id
                instructor = db.session.query(Instructor).filter_by(instructor_id=instructor_id)[0]
                if instructor and check_password_hash(instructor.password, password):
                    session['instructor_id'] = instructor_id
                    return redirect(url_for("ibp.index"))
                elif instructor and instructor.password == password:
                    # 如果用户密码是密文存储，则将密码更改为哈希后的密码
                    instructor.password = generate_password_hash(password)
                    db.session.commit()
                    session['instructor_id'] = instructor_id
                    return redirect(url_for("ibp.index"))
                else:
                    # todo 调用前端接口弹出提示
                    print("学工号或密码错误")
                    return redirect(url_for("login"))

            # 都不是
            else:
                return "未知用户错误"
        else:
            return "学工号或密码格式错误"


if __name__ == '__main__':
    app.run()
