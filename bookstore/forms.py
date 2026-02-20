from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Length, EqualTo, InputRequired, Regexp


class LoginForm(FlaskForm):
    """客户登录页面中的表单"""

    userid = StringField(
        "客户账号:",
        validators=[
            Length(min=3, max=10, message="客户账号长度必须在3到10位"),
            InputRequired("客户账号必须输入"),
        ],
    )
    password = PasswordField(
        "客户密码:", validators=[InputRequired("客户姓名必须输入")]
    )


class CustomerRegForm(FlaskForm):
    """客户注册页面中的表单"""

    userid = StringField(
        label="客户账号",
        validators=[
            Length(min=3, max=10, message="客户账号长度必须在3到10位"),
            InputRequired("客户账号必须输入"),
        ],
    )
    name = StringField(
        label="客户姓名:",
        validators=[
            Length(min=3, max=10, message="客户姓名长度必须在3到10位"),
            InputRequired("客户姓名必须输入"),
        ],
    )
    password = PasswordField(
        label="客户密码:",
        validators=[
            Length(min=6, max=10, message="客户密码长度必须在6到10位"),
            InputRequired("客户密码必须输入"),
        ],
    )
    password2 = PasswordField(
        label="再次输入密码:",
        validators=[
            Length(min=6, max=10, message="客户密码长度必须在6到10位"),
            EqualTo("password", message="两次输入的密码不一致"),
        ],
    )

    # 验证日期的正则表达式 YYYY-MM-DD YY-MM-DD
    reg_date = r"^(((19|20)(([02468][048])|([13579][26]))-02-29)|((20[0-9][0-9])|(19[0-9][0-9]))-(((0[1-9])|(1[0-2]))-((0[1-9])|(\d)|(2[0-8])))|((((0[13578])|(1[02]))-(31))|(((0[1,3-9])|(1[0-2]))-(29|30))))$"
    birthday = StringField(
        label="出生日期:", validators=[Regexp(reg_date, message="输入的日期无效")]
    )
    address = StringField(label="通信地址:")
    phone = StringField(label="电话号码:")
