# 网上图书商城系统使用文档

## 项目简介

这是一个基于 Flask 框架开发的网上图书商城系统，提供用户注册、登录、商品浏览、购物车管理、订单提交等功能。

## 环境要求

- Python 3.11 或更高版本
- pip 包管理器

## 安装步骤

### 1. 安装依赖

在项目根目录下执行以下命令安装所需的依赖包：

```bash
pip install -r requirements.txt
```

依赖包包括：
- Flask==3.0.0
- Flask-WTF==1.2.1
- Flask-SQLAlchemy==3.1.1
- WTForms==3.1.1

### 2. 数据库初始化

#### 创建数据库表

```bash
python -m flask create-tables
```

#### 加载初始数据

```bash
python -m flask load-data
```

初始数据包含5本图书信息，用于测试。

## 运行项目

### 启动服务器

在项目根目录下执行：

```bash
python app.py
```

服务器将在 http://127.0.0.1:5000 启动。

### 访问系统

在浏览器中打开：http://127.0.0.1:5000

## 功能说明

### 1. 用户注册

- 访问注册页面：http://127.0.0.1:5000/reg/
- 填写以下信息：
  - 客户账号（3-10位字符）
  - 客户姓名（3-10位字符）
  - 客户密码（6-10位字符）
  - 确认密码
  - 出生日期（格式：YYYY-MM-DD）
  - 通信地址（可选）
  - 电话号码（可选）
- 点击"提交"按钮完成注册

### 2. 用户登录

- 访问登录页面：http://127.0.0.1:5000/login/
- 输入客户账号和密码
- 点击"登录"按钮

### 3. 主页面

登录成功后进入主页面，可以访问以下功能：
- 商品列表
- 购物车

### 4. 商品列表

- 显示所有可售图书
- 每本书显示：
  - 商品名称
  - 商品价格
  - 添加到购物车按钮
- 点击商品名称可查看详细信息

### 5. 商品详情

显示图书的详细信息：
- 商品图片
- 一口价
- 作者
- 出版社
- ISBN
- 版次
- 开本
- 出版时间
- 用纸
- 包装
- 添加到购物车按钮

### 6. 购物车

- 显示已添加的商品
- 可以修改商品数量
- 自动计算小计和总价
- 点击"提交订单"完成购买

### 7. 订单提交

- 确认购物车中的商品和数量
- 点击"提交订单"按钮
- 系统生成订单号
- 显示订单完成页面

### 8. 我的账号

查看个人账户信息：
- 客户账号
- 客户姓名
- 出生日期
- 通信地址
- 电话号码

## 使用流程

1. **首次使用**：注册账号
2. **登录系统**：使用账号密码登录
3. **浏览商品**：查看商品列表，选择感兴趣的商品
4. **查看详情**：点击商品名称查看详细信息
5. **添加购物车**：将商品添加到购物车
6. **管理购物车**：查看购物车，调整商品数量
7. **提交订单**：确认订单信息，提交订单
8. **查看账户**：在"我的账号"页面查看个人信息

## 数据库结构

### customers（客户表）
- id：客户账号（主键）
- name：客户姓名
- password：客户密码
- address：通信地址
- phone：电话号码
- birthday：出生日期

### goods（商品表）
- goods_id：商品ID（主键）
- name：商品名称
- author：作者
- press：出版社
- isbn：ISBN号
- edition：版次
- packaging：包装
- format：开本
- publication_time：出版时间
- paper：用纸
- price：价格
- description：商品描述
- image：商品图片

### orders（订单表）
- orders_id：订单ID（主键）
- order_date：订单日期
- status：订单状态（1-待付款，0-已付款）
- total：订单总额

### order_line_items（订单明细表）
- id：明细ID（主键）
- goods_id：商品ID（外键）
- orders_id：订单ID（外键）
- quantity：商品数量
- sub_total：小计金额

## 注意事项

1. **密码安全**：请妥善保管账号密码
2. **数据备份**：定期备份数据库文件（db/database.db）
3. **浏览器兼容性**：建议使用现代浏览器（Chrome、Firefox、Edge等）
4. **会话超时**：长时间不操作可能导致会话失效，需要重新登录
5. **商品图片**：商品图片存放在 static/goods_images/ 目录下

## 技术栈

- **后端框架**：Flask 3.0.0
- **数据库**：SQLite
- **ORM**：Flask-SQLAlchemy
- **表单验证**：Flask-WTF + WTForms
- **模板引擎**：Jinja2

## 项目结构

```
bookstore/
├── app.py                  # 主应用文件
├── config.py               # 配置文件
├── exts.py                 # 数据库扩展
├── models.py               # 数据模型
├── forms.py                # 表单定义
├── commands.py             # Flask命令
├── requirements.txt        # 依赖包列表
├── db/                     # 数据库目录
│   ├── database.db         # SQLite数据库文件
│   ├── dbhelper.py         # 数据库辅助函数
│   ├── store-schema.sql    # 数据库表结构
│   └── store-dataload.sql  # 初始数据
├── templates/              # 模板目录
│   ├── base_header.html    # 基础模板（带头部）
│   ├── base_title.html     # 基础模板（带标题）
│   ├── login.html          # 登录页面
│   ├── customer_reg.html   # 注册页面
│   ├── customer_reg_success.html  # 注册成功页面
│   ├── main.html           # 主页面
│   ├── goods_list.html     # 商品列表
│   ├── goods_detail.html   # 商品详情
│   ├── goods_header.html   # 商品头部导航
│   ├── cart.html           # 购物车
│   ├── order_finish.html   # 订单完成
│   └── user.html           # 用户信息
└── static/                 # 静态文件目录
    ├── css/
    │   └── public.css      # 公共样式
    ├── images/             # 图片资源
    └── goods_images/       # 商品图片
```

## 常见问题

### Q: 忘记密码怎么办？
A: 当前版本不支持密码找回功能，需要重新注册账号。

### Q: 如何清空购物车？
A: 提交订单后会自动清空购物车，或者关闭浏览器清除会话。

### Q: 可以修改订单吗？
A: 当前版本不支持订单修改功能。

### Q: 如何添加更多商品？
A: 可以直接在数据库中插入商品数据，或修改 db/store-dataload.sql 文件后重新加载数据。

### Q: 端口被占用怎么办？
A: 修改 app.py 文件最后一行，指定其他端口：
```python
app.run(debug=True, port=8000)
```

## 开发者信息

- 开发语言：Python
- Web框架：Flask
- 数据库：SQLite

## 版本历史

- v1.0.0 - 初始版本
  - 用户注册和登录
  - 商品浏览和详情
  - 购物车管理
  - 订单提交
  - 用户信息查看