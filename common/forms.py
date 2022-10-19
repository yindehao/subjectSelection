import wtforms
from wtforms.validators import length


# 登录表单
class LoginForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=10, max=16)])
    password = wtforms.StringField(validators=[length(min=8, max=20)])


# 注册表单
class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=10, max=16)])
    password = wtforms.StringField(validators=[length(min=8, max=20)])