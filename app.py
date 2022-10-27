from flask import Flask, session, url_for, redirect
from flask_mail import Message

from common import config
from common.ext import db, cors, mail
from views import student_bp
from views import subject_bp
from views import teacher_bp

# 初始化app，从文件中导入配置
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
cors.init_app(app)
mail.init_app(app)


# 注册路由视图
app.register_blueprint(student_bp)
app.register_blueprint(subject_bp)
app.register_blueprint(teacher_bp)


# 测试数据库连接
@app.route('/test_connection')
def test_connection():
    # 测试数据库连接，查询当前时间
    now = db.session.execute('SELECT SYSDATE()').first()[0]
    print(f'当前时间为 {now}')
    return f'当前时间为 {now}'


# 测试邮件
@app.route('/test_mail')
def test_mail():
    msg = Message()
    msg.sender = config.MAIL_DEFAULT_SENDER
    msg.subject = "发送邮件测试"
    msg.recipients = ["yindehao@ustc.edu"]
    html_file = open(r"templates/测试.html", encoding="utf-8")
    msg.html = html_file.read()
    mail.send(msg)
    return 'Hello World!'


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


if __name__ == '__main__':
    # 如果是开发模式，本地运行
    # 不是开发模式， 运行云服务器
    if config.SSS_DEV:
        app.run()
    else:
        app.run(host='0.0.0.0', port=5000)
