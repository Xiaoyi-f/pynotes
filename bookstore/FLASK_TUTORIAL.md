# Flask网上图书商城 - 新手入门教程

## 前言

欢迎来到Flask世界！本教程将带你从零开始，通过一个完整的网上图书商城项目，快速掌握Flask框架的核心概念和实战技巧。

## 学习目标

- 理解Flask框架的基本概念
- 掌握Flask的路由、模板、表单等核心功能
- 学会使用Flask-SQLAlchemy进行数据库操作
- 了解会话管理和用户认证
- 能够独立开发简单的Web应用

## 前置知识

- Python基础语法（变量、函数、类、条件语句、循环等）
- HTML基础（了解标签和基本结构）

---

## 第一章：Flask基础入门

### 1.1 什么是Flask？

Flask是一个轻量级的Python Web框架，被称为"微框架"。它简单易学，但功能强大，非常适合初学者入门Web开发。

**Flask的特点：**
- 轻量级：核心代码简洁，易于理解
- 灵活性强：可以根据需要选择各种扩展
- 易于上手：学习曲线平缓
- 社区活跃：有丰富的第三方库支持

### 1.2 第一个Flask应用

让我们看一个最简单的Flask应用：

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '你好，Flask！'

if __name__ == '__main__':
    app.run(debug=True)
```

**代码解析：**

1. `from flask import Flask` - 导入Flask类
2. `app = Flask(__name__)` - 创建Flask应用实例
   - `__name__` 是Python内置变量，表示当前模块名
3. `@app.route('/')` - 路由装饰器
   - 定义URL路径与函数的映射关系
   - `'/'` 表示网站的根路径
4. `def hello():` - 视图函数
   - 处理请求并返回响应
5. `app.run(debug=True)` - 启动应用
   - `debug=True` 开启调试模式，修改代码会自动重启

**运行应用：**
```bash
python app.py
```
然后在浏览器访问 http://127.0.0.1:5000

### 1.3 路由详解

路由是URL到Python函数的映射。Flask使用装饰器来定义路由。

```python
@app.route('/hello')
def hello_world():
    return 'Hello World'

@app.route('/user/<username>')
def show_user_profile(username):
    return f'用户: {username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'文章ID: {post_id}'
```

**路由参数类型：**
- `<string:name>` - 字符串（默认）
- `<int:id>` - 整数
- `<float:price>` - 浮点数
- `<path:subpath>` - 路径（包含斜杠）

### 1.4 HTTP方法

默认情况下，路由只响应GET请求。如果需要处理POST请求：

```python
from flask import request

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return '处理登录'
    return '显示登录表单'
```

---

## 第二章：模板引擎

### 2.1 什么是模板？

模板是包含占位符的HTML文件，Flask使用Jinja2模板引擎将动态数据填充到模板中。

### 2.2 基本模板使用

**创建模板文件：** `templates/index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>
    <p>欢迎，{{ user }}！</p>
</body>
</html>
```

**在Python中使用模板：**

```python
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html', 
                         title='首页',
                         user='张三')
```

**`render_template()` 函数：**
- 第一个参数：模板文件名（在templates目录下）
- 后续参数：传递给模板的变量

### 2.3 模板继承

模板继承可以避免重复代码，创建一个基础模板：

**基础模板：** `templates/base.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}默认标题{% endblock %}</title>
</head>
<body>
    <div class="header">网站头部</div>
    
    {% block content %}
    <p>这是默认内容</p>
    {% endblock %}
    
    <div class="footer">网站底部</div>
</body>
</html>
```

**子模板：** `templates/index.html`

```html
{% extends "base.html" %}

{% block title %}
首页
{% endblock %}

{% block content %}
<h1>欢迎来到首页</h1>
<p>这是首页的内容</p>
{% endblock %}
```

**模板继承语法：**
- `{% extends "base.html" %}` - 继承基础模板
- `{% block name %}...{% endblock %}` - 定义可替换的块

### 2.4 模板中的控制结构

**条件语句：**

```html
{% if user %}
    <p>欢迎，{{ user }}！</p>
{% else %}
    <p>请登录</p>
{% endif %}
```

**循环语句：**

```html
<ul>
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}
</ul>
```

**循环中的特殊变量：**
- `loop.index` - 当前循环索引（从1开始）
- `loop.index0` - 当前循环索引（从0开始）
- `loop.first` - 是否是第一次循环
- `loop.last` - 是否是最后一次循环

---

## 第三章：表单处理

### 3.1 表单基础

**HTML表单：**

```html
<form action="/login" method="post">
    <input type="text" name="username">
    <input type="password" name="password">
    <input type="submit" value="登录">
</form>
```

**Flask处理表单：**

```python
from flask import request

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return f'用户名: {username}, 密码: {password}'
    return render_template('login.html')
```

**`request` 对象：**
- `request.form` - POST表单数据
- `request.args` - URL查询参数
- `request.method` - HTTP方法

### 3.2 使用Flask-WTF处理表单

Flask-WTF提供了表单验证功能，让表单处理更安全、更简单。

**安装依赖：**
```bash
pip install Flask-WTF WTForms
```

**定义表单类：** `forms.py`

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField(
        '用户名',
        validators=[
            DataRequired('用户名不能为空'),
            Length(min=3, max=20, message='用户名长度为3-20个字符')
        ]
    )
    password = PasswordField(
        '密码',
        validators=[
            DataRequired('密码不能为空'),
            Length(min=6, message='密码至少6个字符')
        ]
    )
    submit = SubmitField('登录')
```

**在视图中使用表单：**

```python
from flask import render_template, redirect, url_for
from forms import LoginForm

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # 处理登录逻辑
        return redirect(url_for('index'))
    
    return render_template('login.html', form=form)
```

**在模板中渲染表单：**

```html
<form method="post">
    {{ form.hidden_tag() }}
    
    <p>
        {{ form.username.label }}<br>
        {{ form.username() }}
    </p>
    
    <p>
        {{ form.password.label }}<br>
        {{ form.password() }}
    </p>
    
    <p>{{ form.submit() }}</p>
</form>
```

**常用验证器：**
- `DataRequired()` - 必填
- `Length(min, max)` - 长度限制
- `Email()` - 邮箱格式
- `EqualTo('field')` - 与另一个字段相等
- `Regexp(pattern)` - 正则表达式匹配

---

## 第四章：数据库操作

### 4.1 Flask-SQLAlchemy简介

Flask-SQLAlchemy是Flask的SQLAlchemy扩展，提供了ORM（对象关系映射）功能，让我们用Python类来操作数据库。

**安装依赖：**
```bash
pip install Flask-SQLAlchemy
```

### 4.2 配置数据库

**配置文件：** `config.py`

```python
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

**初始化数据库：** `exts.py`

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

**在应用中初始化：** `app.py`

```python
from flask import Flask
from config import Config
from exts import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
```

### 4.3 定义数据模型

**模型定义：** `models.py`

```python
from exts import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'
```

**字段类型：**
- `db.Integer` - 整数
- `db.String(n)` - 字符串（最大长度n）
- `db.Text` - 长文本
- `db.DateTime` - 日期时间
- `db.Float` - 浮点数
- `db.Boolean` - 布尔值

**字段参数：**
- `primary_key=True` - 主键
- `unique=True` - 唯一
- `nullable=False` - 不能为空
- `default=value` - 默认值

### 4.4 数据库操作

**创建表：**

```python
with app.app_context():
    db.create_all()
```

**添加数据：**

```python
user = User(username='张三', email='zhangsan@example.com', password='123456')
db.session.add(user)
db.session.commit()
```

**查询数据：**

```python
# 查询所有用户
users = User.query.all()

# 根据ID查询
user = User.query.get(1)

# 根据条件查询
user = User.query.filter_by(username='张三').first()

# 模糊查询
users = User.query.filter(User.username.like('%张%')).all()

# 排序
users = User.query.order_by(User.id.desc()).all()

# 限制数量
users = User.query.limit(10).all()
```

**更新数据：**

```python
user = User.query.get(1)
user.email = 'newemail@example.com'
db.session.commit()
```

**删除数据：**

```python
user = User.query.get(1)
db.session.delete(user)
db.session.commit()
```

---

## 第五章：会话管理

### 5.1 什么是会话（Session）？

会话用于在多个请求之间存储用户信息。Flask的session是基于签名的cookie，可以安全地存储数据。

### 5.2 配置Session

**配置密钥：**

```python
app.secret_key = 'your-secret-key-here'
```

或者使用随机密钥：

```python
import os
app.secret_key = os.urandom(24)
```

### 5.3 使用Session

**设置Session：**

```python
from flask import session

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    session['username'] = username
    session['logged_in'] = True
    return '登录成功'
```

**获取Session：**

```python
@app.route('/profile')
def profile():
    if 'username' in session:
        return f'欢迎，{session["username"]}'
    return '请先登录'
```

**删除Session：**

```python
@app.route('/logout')
def logout():
    session.clear()
    return '已退出登录'
```

**检查登录状态：**

```python
@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return '仪表盘页面'
```

---

## 第六章：项目实战 - 网上图书商城

### 6.1 项目结构

```
bookstore/
├── app.py              # 主应用文件
├── config.py           # 配置文件
├── exts.py            # 数据库扩展
├── models.py          # 数据模型
├── forms.py           # 表单定义
├── commands.py        # Flask命令
├── requirements.txt   # 依赖包
├── db/                # 数据库目录
├── templates/         # 模板目录
└── static/            # 静态文件目录
```

### 6.2 核心代码解析

#### 6.2.1 应用初始化

**app.py**

```python
from flask import Flask, request, session, render_template, redirect, url_for, flash
from exts import db
from flask_wtf import CSRFProtect
from forms import CustomerRegForm, LoginForm
from models import Customer, Goods, Orders, OrderLineItem
from commands import init_app
import config

app = Flask(__name__)
app.config.from_object(config)
csrf = CSRFProtect()
csrf.init_app(app)
db.init_app(app)
init_app(app)
```

**解析：**
- 导入所有需要的模块
- 创建Flask应用实例
- 加载配置
- 启用CSRF保护（防止跨站请求伪造）
- 初始化数据库
- 注册自定义命令

#### 6.2.2 用户注册

```python
@app.route("/reg/", methods=["GET", "POST"])
def register():
    form = CustomerRegForm()
    if request.method == "POST":
        if form.validate():
            new_customer = Customer()
            new_customer.id = form.userid.data
            new_customer.name = form.name.data
            new_customer.password = form.password.data
            new_customer.address = form.address.data
            new_customer.birthday = form.birthday.data
            new_customer.phone = form.phone.data
            db.session.add(new_customer)
            db.session.commit()
            return render_template("customer_reg_success.html", form=form)
    return render_template("customer_reg.html", form=form)
```

**流程解析：**
1. 创建表单实例
2. 检查是否为POST请求
3. 验证表单数据
4. 创建Customer对象并赋值
5. 添加到数据库会话
6. 提交到数据库
7. 返回成功页面

#### 6.2.3 用户登录

```python
@app.route("/")
@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            c = db.session.query(Customer).filter_by(id=form.userid.data).first()
            if c is not None and c.password == form.password.data:
                customer = {}
                customer["id"] = c.id
                customer["name"] = c.name
                customer["password"] = c.password
                customer["address"] = c.address
                customer["phone"] = c.phone
                customer["birthday"] = c.birthday
                session["customer"] = customer
                return redirect(url_for("main"))
            else:
                flash("您输入的客户账号和密码错误.")
                return render_template("login.html", form=form)
    return render_template("login.html", form=form)
```

**流程解析：**
1. 创建登录表单
2. 验证表单数据
3. 查询数据库中的用户
4. 验证密码
5. 将用户信息存入session
6. 重定向到主页面

**关键点：**
- `filter_by()` - 根据字段值查询
- `first()` - 获取第一条记录
- `session[]` - 存储会话数据
- `flash()` - 显示提示信息
- `redirect()` - 重定向到其他页面
- `url_for()` - 根据视图函数名生成URL

#### 6.2.4 商品列表

```python
@app.route("/list/")
def show_goods_list():
    if "customer" not in session.keys():
        flash("您还没有登录,请登录.")
        return redirect(url_for("login"))
    goodslist = db.session.query(Goods).all()
    return render_template("goods_list.html", list=goodslist)
```

**流程解析：**
1. 检查用户是否登录
2. 查询所有商品
3. 渲染商品列表模板

#### 6.2.5 添加购物车

```python
@app.route("/add/")
def add_cart():
    if "customer" not in session.keys():
        flash("您还没有登录,请登录.")
        return redirect(url_for("login"))
    
    goodsid = int(request.args["id"])
    goodsname = request.args["name"]
    goodsprice = float(request.args["price"])
    
    if "cart" not in session.keys():
        session["cart"] = []
    
    cart = session["cart"]
    flag = 0
    for item in cart:
        if item[0] == goodsid:
            item[3] += 1
            flag = 1
            break
    
    if flag == 0:
        cart.append([goodsid, goodsname, goodsprice, 1])
    
    session["cart"] = cart
    flash("已经添加商品【" + goodsname + "】到购物车")
    
    return redirect(url_for("show_goods_list"))
```

**流程解析：**
1. 检查登录状态
2. 从URL参数获取商品信息
3. 初始化购物车
4. 检查商品是否已在购物车
5. 如果存在则增加数量，否则添加新商品
6. 更新session
7. 显示提示信息

**购物车数据结构：**
```python
cart = [
    [goods_id, goods_name, goods_price, quantity],
    [goods_id, goods_name, goods_price, quantity],
    ...
]
```

#### 6.2.6 查看购物车

```python
@app.route("/cart/")
def show_cart():
    if "customer" not in session.keys():
        flash("您还没有登录,请登录.")
        return redirect(url_for("login"))
    
    if "cart" not in session.keys():
        return render_template("cart.html", list=[], total=0.0)
    
    cart = session["cart"]
    list = []
    total = 0.0
    
    for item in cart:
        subtotal = item[2] * item[3]
        total += subtotal
        new_item = (item[0], item[1], item[2], item[3], subtotal)
        list.append(new_item)
    
    return render_template("cart.html", list=list, total=total)
```

**流程解析：**
1. 检查登录状态
2. 检查购物车是否存在
3. 遍历购物车计算小计和总价
4. 渲染购物车页面

#### 6.2.7 提交订单

```python
@app.route("/submit_order/", methods=["POST"])
def submit_order():
    orders = Orders()
    n = random.randint(0, 9)
    d = datetime.datetime.today()
    orderid = int(d.timestamp() * 1e6) + n
    orders.id = orderid
    orders.orderdate = d.strftime("%Y-%m-%d %H:%M:%S")
    orders.status = 1
    db.session.add(orders)
    
    cart = session["cart"]
    total = 0.0
    
    for item in cart:
        quantity = request.form["quantity_" + str(item[0])]
        try:
            quantity = int(quantity)
        except:
            quantity = 0
        
        subtotal = item[2] * quantity
        total += subtotal
        
        order_line_item = OrderLineItem()
        order_line_item.quantity = quantity
        order_line_item.goods_id = item[0]
        order_line_item.orders_id = orderid
        order_line_item.subtotal = subtotal
        db.session.add(order_line_item)
    
    orders.total = total
    db.session.commit()
    session.pop("cart", None)
    
    return render_template("order_finish.html", orderid=orderid)
```

**流程解析：**
1. 创建订单对象
2. 生成订单ID
3. 设置订单日期和状态
4. 添加订单到数据库
5. 遍历购物车创建订单明细
6. 计算总价
7. 提交到数据库
8. 清空购物车
9. 返回订单完成页面

### 6.3 模板示例

#### 6.3.1 商品列表模板

```html
{% extends "base_title.html" %}
{% block title %}商品列表{% endblock %}
{% block body %}
    <table width="100%" border="0" align="center">
        <tr bgcolor="#b4c8ed">
            <th>商品名称</th>
            <th>商品价格</th>
            <th>添加到购物车</th>
        </tr>
        {% for goods in list %}
            <tr bgcolor={{ loop.cycle('#ffffff', '#edf8ff') }}>
                <td><a href="/detail?id={{ goods.id }}">{{ goods.description }}</a></td>
                <td>¥{{ goods.price }}</td>
                <td><a href="/add?id={{ goods.id }}&name={{ goods.name }}&price={{ goods.price }}">添加到购物车</a></td>
            </tr>
        {% endfor %}
    </table>
{% endblock %}
```

**关键点：**
- `{% extends %}` - 继承基础模板
- `{% block %}` - 定义内容块
- `{% for %}` - 循环遍历
- `{{ }}` - 输出变量
- `loop.cycle()` - 循环交替值

#### 6.3.2 购物车模板

```html
{% extends "base_title.html" %}
{% block title %}购物车{% endblock %}
{% block body %}
    <form action="/submit_order" method="post">
        <table width="100%" border="0" align="center">
            <tr bgcolor="#A5D3FF">
                <td>商品名称</td>
                <td>数量</td>
                <td>单价</td>
                <td>小计</td>
            </tr>
            {% for item in list %}
            <tr>
                <td>{{ item[1] }}</td>
                <td>
                    <input name="quantity_{{item[0]}}" type="text" value="{{item[3]}}"/>
                </td>
                <td>¥{{ item[2] }}</td>
                <td>¥{{ item[4] }}</td>
            </tr>
            {% endfor %}
            <tr>
                <td colspan="4" align="right">合计: ¥{{ total }}</td>
            </tr>
        </table>
        <div align="center">
            <input type="image" src="{{ url_for('static', filename='images/submit_order.jpg') }}"/>
        </div>
    </form>
{% endblock %}
```

**关键点：**
- 表单提交到 `/submit_order`
- 动态生成输入框名称 `quantity_{{item[0]}}`
- `url_for()` 生成静态文件URL

---

## 第七章：进阶技巧

### 7.1 Flash消息

Flash消息用于在请求之间传递临时消息（如成功提示、错误信息）。

```python
from flask import flash

@app.route('/login', methods=['POST'])
def login():
    if login_success:
        flash('登录成功！', 'success')
        return redirect(url_for('index'))
    else:
        flash('用户名或密码错误！', 'error')
        return render_template('login.html')
```

**在模板中显示Flash消息：**

```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="alert alert-{{ category }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

### 7.2 URL生成

使用 `url_for()` 函数生成URL，而不是硬编码URL路径。

```python
# 硬编码（不推荐）
return redirect('/user/profile')

# 使用url_for（推荐）
return redirect(url_for('user_profile', user_id=1))

# 带参数的URL
url_for('show_post', post_id=1)  # /post/1
```

**优点：**
- 修改路由时不需要修改代码
- 自动处理URL编码
- 支持外部URL

### 7.3 静态文件

静态文件（CSS、JavaScript、图片）放在 `static` 目录下。

**目录结构：**
```
static/
├── css/
│   └── style.css
├── js/
│   └── script.js
└── images/
    └── logo.png
```

**在模板中引用：**

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/script.js') }}"></script>
<img src="{{ url_for('static', filename='images/logo.png') }}">
```

### 7.4 错误处理

自定义错误页面：

```python
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
```

---

## 第八章：调试与部署

### 8.1 调试模式

```python
app.run(debug=True)
```

**调试模式功能：**
- 代码修改后自动重启
- 显示详细的错误信息
- 提供调试器

### 8.2 日志记录

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    logger.info('访问首页')
    return 'Hello'
```

### 8.3 生产环境部署

**使用Gunicorn部署：**

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

**使用Nginx作为反向代理：**

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 第九章：学习建议

### 9.1 学习路径

1. **基础阶段**（1-2周）
   - 掌握Flask基础概念
   - 理解路由和视图函数
   - 学会使用模板

2. **进阶阶段**（2-3周）
   - 学习数据库操作
   - 掌握表单处理
   - 理解会话管理

3. **实战阶段**（3-4周）
   - 完成完整项目
   - 学习部署
   - 优化代码

### 9.2 推荐资源

**官方文档：**
- Flask官方文档：https://flask.palletsprojects.com/
- Flask-SQLAlchemy文档：https://flask-sqlalchemy.palletsprojects.com/
- WTForms文档：https://wtforms.readthedocs.io/

**学习网站：**
- Flask中文文档：https://dormousehole.readthedocs.io/
- 廖雪峰的Flask教程

**练习项目：**
- 个人博客
- 待办事项应用
- 在线聊天室
- 电商网站

### 9.3 常见问题

**Q: Flask和Django有什么区别？**
A: Flask是微框架，灵活轻量；Django是全功能框架，功能齐全但学习曲线较陡。

**Q: 如何选择数据库？**
A: 小项目推荐SQLite，中大型项目推荐MySQL或PostgreSQL。

**Q: 如何处理用户认证？**
A: 可以使用Flask-Login扩展，它提供了完整的用户认证功能。

**Q: 如何防止CSRF攻击？**
A: 使用Flask-WTF的CSRF保护，它会自动处理CSRF令牌。

---

## 第十章：总结

通过本教程，你已经掌握了：

1. Flask框架的核心概念和基本用法
2. 路由、模板、表单等核心功能
3. Flask-SQLAlchemy数据库操作
4. 会话管理和用户认证
5. 完整项目的开发流程

### 下一步学习

- Flask-RESTful - 开发RESTful API
- Flask-Login - 用户认证
- Flask-Migrate - 数据库迁移
- Flask-Admin - 后台管理
- Celery - 异步任务处理

### 继续加油！

Flask是一个强大的框架，掌握它将为你打开Web开发的大门。继续实践，不断学习，你一定能成为一名优秀的Flask开发者！

---

## 附录：常用命令速查

### Flask命令

```bash
# 运行应用
python app.py

# Flask shell（交互式环境）
flask shell

# 运行测试
flask test

# 数据库迁移
flask db init
flask db migrate -m "message"
flask db upgrade
```

### Git命令

```bash
# 初始化仓库
git init

# 添加文件
git add .

# 提交
git commit -m "message"

# 推送到远程
git push origin main
```

### pip命令

```bash
# 安装包
pip install package-name

# 安装依赖
pip install -r requirements.txt

# 卸载包
pip uninstall package-name

# 查看已安装的包
pip list
```

---

**祝你学习愉快！** 🎉