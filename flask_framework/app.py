# -*- coding: utf-8 -*-
"""
Flask框架完整学习示例 - 工作必知必会
作者: Lingma
用途: 展示Flask框架的核心功能和最佳实践

本项目涵盖:
1. 基础路由和视图函数
2. 模板渲染和Jinja2语法
3. 表单处理和数据验证
4. 数据库集成(SQLAlchemy)
5. 用户认证和会话管理
6. RESTful API开发
7. 错误处理和日志记录
8. 配置管理和部署准备
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
import os
import logging
from datetime import datetime

# ==================== 1. 应用初始化和配置 ====================
# 创建Flask应用实例
app = Flask(__name__)

# 基础配置
app.config['SECRET_KEY'] = 'your-secret-key-here'  # 用于CSRF保护和会话加密
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_demo.db'  # SQLite数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭修改跟踪以节省内存

# 初始化扩展
db = SQLAlchemy(app)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        logging.FileHandler('flask_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==================== 2. 数据库模型定义 ====================
class User(db.Model):
    """用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """设置密码哈希"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    """文章模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系定义
    author = db.relationship('User', backref=db.backref('posts', lazy=True))
    
    def __repr__(self):
        return f'<Post {self.title}>'

# ==================== 3. 表单定义 ====================
class LoginForm(FlaskForm):
    """登录表单"""
    username = StringField('用户名', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    """注册表单"""
    username = StringField('用户名', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('确认密码', 
                                   validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

class PostForm(FlaskForm):
    """文章发布表单"""
    title = StringField('标题', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('内容', validators=[DataRequired()])
    submit = SubmitField('发布')

# ==================== 4. 路由和视图函数 ====================

@app.route('/')
def index():
    """
    首页路由
    展示所有文章列表
    """
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    """关于我们页面"""
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    用户登录功能
    GET: 显示登录表单
    POST: 处理登录请求
    """
    if session.get('user_id'):
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('登录成功！', 'success')
            logger.info(f"用户 {user.username} 登录成功")
            return redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误', 'danger')
            logger.warning(f"用户 {form.username.data} 登录失败")
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    用户注册功能
    """
    if session.get('user_id'):
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # 检查用户名和邮箱是否已存在
        if User.query.filter_by(username=form.username.data).first():
            flash('用户名已存在', 'danger')
            return render_template('register.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('邮箱已被注册', 'danger')
            return render_template('register.html', form=form)
        
        # 创建新用户
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('注册成功！请登录', 'success')
        logger.info(f"新用户 {form.username.data} 注册成功")
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    """用户登出"""
    session.clear()
    flash('已安全退出', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """用户仪表板"""
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    posts = Post.query.filter_by(author_id=user.id).order_by(Post.created_at.desc()).all()
    return render_template('dashboard.html', user=user, posts=posts)

@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    """创建新文章"""
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author_id=session['user_id']
        )
        db.session.add(post)
        db.session.commit()
        flash('文章发布成功！', 'success')
        logger.info(f"用户 {session['username']} 发布了文章: {post.title}")
        return redirect(url_for('index'))
    
    return render_template('create_post.html', form=form)

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    """文章详情页面"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    """编辑文章"""
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    post = Post.query.get_or_404(post_id)
    
    # 检查权限
    if post.author_id != session['user_id']:
        flash('您没有权限编辑此文章', 'danger')
        return redirect(url_for('post_detail', post_id=post_id))
    
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('文章更新成功！', 'success')
        logger.info(f"用户 {session['username']} 更新了文章: {post.title}")
        return redirect(url_for('post_detail', post_id=post.id))
    
    return render_template('edit_post.html', form=form, post=post)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """删除文章"""
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    post = Post.query.get_or_404(post_id)
    
    # 检查权限
    if post.author_id != session['user_id']:
        flash('您没有权限删除此文章', 'danger')
        return redirect(url_for('post_detail', post_id=post_id))
    
    db.session.delete(post)
    db.session.commit()
    flash('文章已删除', 'success')
    logger.info(f"用户 {session['username']} 删除了文章: {post.title}")
    return redirect(url_for('index'))

# ==================== 5. RESTful API 接口 ====================
@app.route('/api/posts', methods=['GET'])
def api_get_posts():
    """API: 获取所有文章"""
    posts = Post.query.all()
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'content': post.content[:100] + '...' if len(post.content) > 100 else post.content,
        'author': post.author.username,
        'created_at': post.created_at.isoformat()
    } for post in posts])

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def api_get_post(post_id):
    """API: 获取单篇文章"""
    post = Post.query.get_or_404(post_id)
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': post.author.username,
        'created_at': post.created_at.isoformat()
    })

@app.route('/api/users/<int:user_id>/posts', methods=['GET'])
def api_user_posts(user_id):
    """API: 获取用户的所有文章"""
    posts = Post.query.filter_by(author_id=user_id).all()
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'created_at': post.created_at.isoformat()
    } for post in posts])

# ==================== 6. 错误处理 ====================
@app.errorhandler(404)
def not_found_error(error):
    """404错误处理"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    db.session.rollback()
    return render_template('errors/500.html'), 500

# ==================== 7. 应用初始化 ====================
def init_app():
    """初始化应用"""
    # 创建数据库表
    with app.app_context():
        db.create_all()
        logger.info("数据库初始化完成")
    
    # 创建默认用户（仅用于演示）
    with app.app_context():
        if not User.query.first():
            admin = User(username='admin', email='admin@example.com')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            logger.info("创建默认管理员账户: admin/admin123")

if __name__ == '__main__':
    init_app()
    logger.info("Flask应用启动...")
    # 开发环境下启用调试模式
    app.run(debug=True, host='0.0.0.0', port=5000)