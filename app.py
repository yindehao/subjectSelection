from flask import Flask
from common import config
from common.ext import db

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def hello_world():
    # 测试数据库连接，查询当前时间
    now = db.session.execute('SELECT SYSDATE()').first()[0]
    print(f'当前时间为 {now}')
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
