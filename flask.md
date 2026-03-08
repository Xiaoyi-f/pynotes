1.应用
form flask import Flask, request, render_template, make_response, url_for, jsonify

# Flask的一个对象是WSGI应用
app = Flask(__name__) # 以当前模块作为入口
app.debug = False
# 路由注册
@app.route('/hello/<name>') # app.add_url_rule(‘/’, ‘hello’, hello_world)
def hello_world(name):
    return 'HelloWorld'

@app.route('/num/<int:integer>', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def test_int(integer):
    pass

@app.route('/num/<float:decimal>', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def test_float(decimal):
    pass

@app.route('/pathfor/<path:path>', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def test_path(path):
    pass

@app.route('/string/<string:str>', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def test_string(str):
    pass

@app.route('/test', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def test():
    # request是一个接收用户发送的对象
    if request.method == 'POST':
        # 接收表单数据
        data = request.form.get('name')
        all_data = request.form.to_dict()

        # 接收url中?后面的参数
        page = request.args.get('page', default=6, type=int) # 自动转为int
        all_params = request.args.to_dict()

        # 获取Cookie
        username = request.cookies.get('username')

        # 设置Cookie -> 字典
        resp = make_response('Cookie 已设置!')
        resp.set_cookie('username', 'xiaoyi', max_age=3600) # 单位秒

        # 接收上传的文件
        file = request.files # 字典 -> 键是name属性 值是FileStorage对象
        return render_template('test.html') # 渲染HTML文件

@app.route('/axios', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def axios():
    # axios默认发送json数据
    axios_data = request.json
    name = axios_data.get('key', default='demo')
        
    # 返回成功响应
    return jsonify({
        'status': 'success',
        'message': '用户创建成功',
        'user': {
            'id': new_user.id,
            'name': new_user.name,
            'age': new_user.age,
            'city': new_user.city
        }
    }), 201  # 201 表示已创建

@app.route('/url_for', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def url_for_test():
    print(f"The url of func test: {url_for('test')}")
    return redirect(url_for('test'))

if __name__ == "__main__":
    app.run(127.0.0.1, 5000) # 0.0.0.0使服务器在外部可用
        
file = request.files['avatar']  # 获取 FileStorage 对象

# FileStorage 对象包含：
print(file_obj.filename)      # 实际的文件名: "profile.jpg"
print(file_obj.name)          # 表单字段名: "avatar"
print(file_obj.mimetype)       # 文件类型: "image/jpeg"
print(file_obj.content_type)   # 内容类型: "image/jpeg"
print(file_obj.content_length) # 文件大小: 102400 (字节)
print(file_obj.headers)        # 请求头信息
print(file_obj.stream)         # 底层的文件流

# FileStorage 对象的方法 -> 只读：
file.save('path/to/save')  # 保存文件
file.read(字节数)
file.readline()
file.readlines()
file.seek(+/-字节数, 0/1/2)
file.tell()
file.readable()
file.writable()
file_obj.close()                # 关闭文件
2.Cookies
Cookies以文本形式存储在客户的计算机上，其目的是记住和跟踪与客户使用情况有关的数据，以获取更好的访问者体验和网站统计数据，Cookies同时存储到期时间、路径和站点的域名
Flask中Cookie可以使用request、make_response、set_cookie操作
 # 设置带参数的 cookie
    resp.set_cookie(
        'key', 
        'value',
        max_age=3600,           # 1小时（秒）
        expires=None,           # 可用具体时间/时刻
        path='/',               
        domain='.example.com',
        secure=True,            # 仅 HTTPS
        httponly=True,          # JS 无法读取
        samesite='Strict'       # Lax / Strict / None
    )
3.Sessions
与 Cookie 一样，Session 数据也存储在客户端上。会话是客户端登录服务器和注销服务器的时间间隔，需要在此会话中保存的数据存储在客户端浏览器中
与每个客户的会话被分配一个Session ID. 会话数据存储在 cookie 之上，服务器以加密方式对其进行签名，对于这种加密，Flask 应用程序需要一个已定义的SECRET_KEY.
会话对象也是一个字典对象，包含会话变量和相关值的键值对
# 配置密钥
app.secret_key = 'your-secret-key-here'
# 使用随机密钥
import os
app.secret_key = os.urandom(24)

from flask import session 

session['key'] = 'value'
session.pop('key', None) # None用于避免KeyError
session.clear()
# 获取session内容直接获取即可

4.重定向与请求错误
from flask import Flask, abort, render_template

app = Flask(__name__)

# 自定义 404 错误页面 -> 无对应资源
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# 自定义 403 错误页面 -> 无权限
@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403

# 自定义 500 错误页面 -> 服务器出问题
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

@app.route('/articles/<int:article_id>')
def show_article(article_id):
    article = get_article(article_id)
    if article is None:
        # 会触发上面的 page_not_found 处理器
        abort(404)
    
    return render_template('test.html')
5.配置
app.config 是 Flask 应用的配置对象，就像一个全局设置中心，用来存放整个应用的各种配置参数
建议使用app.config.from_object(模块名)实现配置，需要自己创建一个配置模块，一般叫config.py
import os

DEBUG = True
basedir = os.path.abspath(os.path.dirname(__file__))
# sqlite需要三个斜杠标明URL
SQLALCHEMY_DATABASE_URI = r"sqlite:///" + os.path.join(basedir, "db", "database.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
SECRET_KEY = 'your-secret-key-change-this-in-production-12345678'

6.Flask-Mail
Flask-Mail扩展使设置任何电子邮件服务器的简单界面变得非常容易
pip install Flask-Mail
需要通过设置以下应用程序参数的值来配置 Flask-Mail ->
序号	Parameters & Description
1	MAIL_SERVER
电子邮件服务器的名称/IP 地址
2	MAIL_PORT
使用的服务器端口号
3	MAIL_USE_TLS
启用/禁用传输安全层加密
4	MAIL_USE_SSL
启用/禁用安全套接字层加密
5	MAIL_DEBUG
调试支持。默认是 Flask 应用程序的调试状态
6	MAIL_USERNAME
发件人用户名
7	MAIL_PASSWORD
发件人密码
8	MAIL_DEFAULT_SENDER
设置默认发件人
9	MAIL_MAX_EMAILS
设置要发送的最大邮件数
10	MAIL_SUPPRESS_SEND
如果 app.testing 设置为 true，则发送抑制
11	MAIL_ASCII_ATTACHMENTS
如果设置为 true，附加文件名将转换为 ASCII
flask-mail 模块包含以下重要类的定义 ->
1.邮件类 Mail
Mail类的方法
序号	Methods & Description
1	send()
发送 Message 类对象的内容
2	connect()
打开与邮件主机的连接
3	send_message()
发送消息对象
2.消息类 Message
消息类方法
attach()- 向消息添加附件
该方法采用以下参数 ->
● filename- 要附加的文件名
● content_type− MIME 类型的文件
● data− 原始文件数据
● disposition− 内容处置（如果有）
add_recipient() -> 将另一个收件人添加到消息中
示例如下:
在以下示例中，Google gmail 服务的 SMTP 服务器用作 Flask-Mail 配置的 MAIL_SERVER
Step 1− 从代码中的 flask-mail 模块导入 Mail 和 Message 类
from flask_mail import Mail, Message
Step 2− 然后按照以下设置配置 Flask-Mail
端口	加密方式	说明
465	SSL	从一开始就加密（SMTPS），通常用于 Gmail、QQ 邮箱等
587	TLS/STARTTLS	先建立普通连接，然后升级到加密连接，现代推荐标准
25	无/可选	传统 SMTP 端口，常被 ISP 封锁，用于服务器间转发
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'yourId@gmail.com'
app.config['MAIL_PASSWORD'] = '*****'
app.config['MAIL_USE_TLS'] = False   
app.config['MAIL_USE_SSL'] = True
Step 3− 创建Mail 类的实例
mail = Mail(app)
Step 4− 在由 URL 规则映射的 Python 函数中设置 Message 对象(‘/’)
@app.route("/")
def index():
   msg = Message('Hello', sender = 'yourId@gmail.com', recipients = ['id1@gmail.com'])
   msg.body = "This is the email body"
   mail.send(msg)
   return "Sent"
Step 5- 在 Python Shell 中运行以下脚本并访问http://localhost:5000/
from flask import Flask
from flask_mail import Mail, Message
app =Flask(__name__)
mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'yourId@gmail.com'
app.config['MAIL_PASSWORD'] = '*****'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
@app.route("/")
def index():
   msg = Message('Hello', sender = 'yourId@gmail.com', recipients = ['id1@gmail.com'])
   msg.body = "Hello Flask message sent from Flask-Mail"
   mail.send(msg)
   return "Sent"
if __name__ == '__main__':
   app.run(debug = True)
注意: Gmail 服务中的内置安全功能可能会阻止此登录尝试,您可能必须降低安全级别,请登录您的 Gmail 帐户并访问此链接以降低安全性
7.Flask-WTF
服务器端脚本必须从 http 请求数据重新创建表单元素，所以实际上，表单元素必须定义两次 —— 一次在 HTML 中，另一次在服务器端脚本中
Flask-WTF是一个灵活的表单渲染和验证库
pip install Flask-WTF
安装的包包含一个Form类，它必须用作用户定义表单的父级
WTforms包包含各种表单字段的定义。一些Standard form fields下面列出 -> 
序号	标准表单字段 & 描述
1	TextField
表示 <input type = 'text'> HTML 表单元素
2	BooleanField
表示 <input type = 'checkbox'> HTML 表单元素
3	DecimalField
用于显示带小数的数字的文本字段
4	IntegerField
用于显示整数的 TextField
5	RadioField
表示 <input type = 'radio'> HTML 表单元素
6	SelectField
表示选择表单元素
7	TextAreaField
表示 <testarea> html 表单元素
8	PasswordField
表示 <input type = 'password'> HTML 表单元素
9	SubmitField
表示 <input type = 'submit'> 表单元素
例如，包含文本字段的表单可以设计如下 
from flask_wtf import Form
from wtforms import TextField
class ContactForm(Form):
   name = TextField("Name Of Student")
除了‘name’字段，CSRF 令牌的隐藏字段是自动创建的，这是为了防止Cross Site Request Forgery攻击
渲染后，这将生成一个等效的 HTML 脚本，如下所示 
<input id = "csrf_token" name = "csrf_token" type = "hidden" />
<label for = "name">Name Of Student</label><br>
<input id = "name" name = "name" type = "text" value = "" />
在 Flask 应用程序中使用用户定义的表单类，并使用模板呈现表单
from flask import Flask, render_template
from forms import ContactForm  # 假设ContactForm类已经在forms.py中定义好
app = Flask(__name__)
app.secret_key = 'development key'
@app.route('/contact')
def contact():
   form = ContactForm()
   return render_template('contact.html', form = form)
if __name__ == '__main__':
   app.run(debug = True)
WTForms 包还包含验证器类，在将验证应用于表单字段时很有用，以下列表显示了常用的验证器
序号	Validators Class & Description
1	DataRequired
检查输入字段是否为空
2	Email
检查字段中的文本是否遵循电子邮件 ID 约定
3	IPAddress
验证输入字段中的 IP 地址
4	Length
验证输入字段中的字符串长度是否在给定范围内
5	NumberRange
验证给定范围内输入字段中的数字
6	URL
验证输入字段中输入的 URL
我们现在申请‘DataRequired’的验证规则name联系表格中的字段
name = TextField("Name Of Student",[validators.Required("Please enter your name.")])
validators是验证器，Required方法会在验证不通过时候触发
{% for message in form.name.errors %}
   {{ message }}
{% endfor %}
以下示例演示了上面给出的概念的设计Contact form下面给出(forms.py)
from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField,
   SelectField
from wtforms import validators, ValidationError
class ContactForm(Form):
   name = TextField("Name Of Student",[validators.Required("Please enter 
      your name.")])
   Gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
   Address = TextAreaField("Address")
   
   email = TextField("Email",[validators.Required("Please enter your email address."),
      validators.Email("Please enter your email address.")])
   
   Age = IntegerField("age")
   language = SelectField('Languages', choices = [('cpp', 'C++'), 
      ('py', 'Python')])
   submit = SubmitField("Send")
验证器应用于Name和Email字段
下面给出的是 Flask 应用程序脚本(formexample.py)
from flask import Flask, render_template, request, flash
from forms import ContactForm
app = Flask(__name__)
app.secret_key = 'development key'
@app.route('/contact', methods = ['GET', 'POST'])
def contact():
   form = ContactForm()
   
   if request.method == 'POST':
      if form.validate() == False:
         flash('All fields are required.')
         return render_template('contact.html', form = form)
      else:
         return render_template('success.html')
      elif request.method == 'GET':
         return render_template('contact.html', form = form)
if __name__ == '__main__':
   app.run(debug = True)
模板的脚本(contact.html)如下 
<!doctype html>
<html>
   <body>
      <h2 style = "text-align: center;">Contact Form</h2>
      
      {% for message in form.name.errors %}
         <div>{{ message }}</div>
      {% endfor %}
      
      {% for message in form.email.errors %}
         <div>{{ message }}</div>
      {% endfor %}
      
      <form action = "http://localhost:5000/contact" method = post>
         <fieldset>
            <legend>Contact Form</legend>
            {{ form.hidden_tag() }}
            
            <div style = font-size:20px; font-weight:bold; margin-left:150px;>
               {{ form.name.label }}<br>
               {{ form.name }}
               <br>
               
               {{ form.Gender.label }} {{ form.Gender }}
               {{ form.Address.label }}<br>
               {{ form.Address }}
               <br>
               
               {{ form.email.label }}<br>
               {{ form.email }}
               <br>
               
               {{ form.Age.label }}<br>
               {{ form.Age }}
               <br>
               
               {{ form.language.label }}<br>
               {{ form.language }}
               <br>
               {{ form.submit }}
            </div>
            
         </fieldset>
      </form>
   </body>
</html>
8.SQLite
SQLite3 是一个轻量级、自包含、无服务器、零配置、支持事务的嵌入式关系型数据库引擎，python内置sqlite3
import sqlite3

DB_FILE = "./db/database.db"


def create_tables():
    file_name = "./db/store-schema.sql"
    with open(file_name, "r", encoding="utf-8") as file:
        sql = file.read()
        conn = sqlite3.connect(DB_FILE)
        try:
            conn.executescript(sql)  # conn.execute('对应数据库语句')
            print("数据库初始化成功")
        except Exception as e:
            print("数据库初始化失败")
            print(e)
        finally:
            conn.close()


def load_data():
    file_name = "./db/store-dataload.sql"
    with open(file_name, "r", encoding="utf-8") as file:
        sql = file.read()
        conn = sqlite3.connect(DB_FILE)
        try:
            conn.executescript(sql)
            print("数据库插入成功")
        except Exception as e:
            print("数据库插入失败")
            print(e)
        finally:
            conn.close()

9.SQLAlchemy
一个强大的ORM这为应用程序开发人员提供了 SQL 的全部功能和灵活性，Flask-SQLAlchemy 是 Flask 扩展，可为您的 Flask 应用程序添加对 SQLAlchemy 的支持 -> 方便复杂操作，实际创建可能需要写更多代码
什么是 ORM (Object Relation Mapping)?
大多数编程语言平台都是面向对象的，另一方面，RDBMS 服务器中的数据存储为表，对象关系映射是一种将对象参数映射到底层 RDBMS 表结构的技术，ORM API 提供了执行 CRUD 操作的方法，而无需编写原始 SQL 语句
Tip: 数据库模型操作通常在models.py中处理
● 步骤 1− 安装 Flask-SQLAlchemy 扩展
pip install Flask-SQLAlchemy
步骤 2- 您需要从此模块导入 SQLAlchemy 类
from flask_sqlalchemy import SQLAlchemy
步骤 3− 现在创建一个 Flask 应用程序对象并设置要使用的数据库的 URI 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
步骤 4− 然后创建一个以应用程序对象为参数的 SQLAlchemy 类对象，此对象包含 ORM 操作的辅助函数，它还提供了一个父模型类，使用它来声明用户定义的模型，在下面的片段中，一个students模型被创建
db = SQLAlchemy(app)
class Students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))  
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))
    
    def __init__(self, name, city, addr,pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin
步骤 5− 要创建/使用 URI 中提到的数据库，请运行create_all()方法
db.create_all()
Session对象 -> SQLAlchemy管理所有持久化操作ORM，以下会话方法执行 CRUD 操作 -
  ○ db.session.add（模型对象） 将记录插入映射表
  ○ db.session.delete（模型对象） 从表中删除记录
  ○ db.session.commit （模型对象） 提交并且保存
  ○ model.query.all() 从表中检索所有记录（对应于 SELECT 查询）model -> 占位模型类 -> 例如: Students
Tip: 为避免模块的循环引用，导致python解释器出错，我们经常还创建exts.py来分隔处理某些逻辑
可以使用过滤器属性将过滤器应用于检索到的记录集,示例 -> 查询所有城市为'Hyderabad'的学生记录:
Students.query.filter_by(city = 'Hyderabad').all()
有了这么多的背景知识，现在我们将为我们的应用程序提供视图函数来添加学生数据,应用程序的入口点是show_all()函数绑定到‘/’网址,学生表的记录集作为参数发送到 HTML 模板。模板中的服务器端代码以 HTML 表格形式呈现记录
@app.route('/')
def show_all():
   return render_template('show_all.html', students = students.query.all())
模板的 HTML 脚本(‘show_all.html’)是这样的
<!DOCTYPE html>
<html lang = "en">
   <head></head>
   <body>
      <h3>
         <a href = "{{ url_for('show_all') }}">Comments - Flask 
            SQLAlchemy example</a>
      </h3>
      
      <hr/>
      {%- for message in get_flashed_messages() %}
         {{ message }}
      {%- endfor %}
      
      <h3>Students (<a href = "{{ url_for('new') }}">Add Student
         </a>)</h3>
      
      <table>
         <thead>
            <tr>
               <th>Name</th>
               <th>City</th>
               <th>Address</th>
               <th>Pin</th>
            </tr>
         </thead>
         <tbody>
            {% for student in students %}
               <tr>
                  <td>{{ student.name }}</td>
                  <td>{{ student.city }}</td>
                  <td>{{ student.addr }}</td>
                  <td>{{ student.pin }}</td>
               </tr>
            {% endfor %}
         </tbody>
      </table>
   </body>
</html>
上面的页面包含一个超链接到‘/new’网址映射new()功能,单击后，它会打开一个学生信息表,数据发布到相同的 URLPOST方法
new.html
<!DOCTYPE html>
<html>
   <body>
      <h3>Students - Flask SQLAlchemy example</h3>
      <hr/>
      
      {%- for category, message in get_flashed_messages(with_categories = true) %}
         <div class = "alert alert-danger">
            {{ message }}
         </div>
      {%- endfor %}
      
      <form action = "{{ request.path }}" method = "post">
         <label for = "name">Name</label><br>
         <input type = "text" name = "name" placeholder = "Name" /><br>
         <label for = "email">City</label><br>
         <input type = "text" name = "city" placeholder = "city" /><br>
         <label for = "addr">addr</label><br>
         <textarea name = "addr" placeholder = "addr"></textarea><br>
         <label for = "PIN">City</label><br>
         <input type = "text" name = "pin" placeholder = "pin" /><br>
         <input type = "submit" value = "Submit" />
      </form>
   </body>
</html>
当 http 方法被检测为 POST 时，表单数据被添加到学生表中，应用程序返回到显示添加数据的主页
@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['city'] or not request.form['addr']:
         flash('Please enter all the fields', 'error')
      else:
         student = students(request.form['name'], request.form['city'],
            request.form['addr'], request.form['pin'])
         
         db.session.add(student)
         db.session.commit()
         
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')
下面给出的是完整的应用程序代码(app.py) 
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)
class students(db.Model):
   id = db.Column('student_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   city = db.Column(db.String(50))
   addr = db.Column(db.String(200)) 
   pin = db.Column(db.String(10))
def __init__(self, name, city, addr,pin):
   self.name = name
   self.city = city
   self.addr = addr
   self.pin = pin
@app.route('/')
def show_all():
   return render_template('show_all.html', students = students.query.all() )
@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['city'] or not request.form['addr']:
         flash('Please enter all the fields', 'error')
      else:
         student = students(request.form['name'], request.form['city'],
            request.form['addr'], request.form['pin'])
         
         db.session.add(student)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')
if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
10.终端命令
基本代码示例
import click
from flask.cli import with_appcontext


@click.command("demo-command") # 定义新命令
@with_appcontext # 接通整个项目
def demo_command():
    execfunc()
    click.echo(
        click.style(
            "content",
            配置
        )
    )

def init_app(app):
    app.cli.add_command(demo_command)

click.style配置
参数	可选值	作用
fg	'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'	文字颜色
bg	同上	背景色
bold	True/False	加粗
underline	True/False	下划线
blink	True/False	闪烁
使用
终端中输入: flask 命令





