from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# ============ 工作中真的在用的 ============

# ------------ 1. 连接数据库（只写一次）------------
engine = create_engine(
    "mysql+pymysql://root:123456@localhost/test?charset=utf8mb4",
    pool_size=10,  # 连接池大小
    pool_pre_ping=True,  # 防止死连接
    echo=False,  # 生产环境关掉SQL日志
)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# ------------ 2. 定义表（最常见）------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, index=True)  # 经常查询加索引
    age = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)


# 建表（部署时跑一次）
Base.metadata.create_all(engine)


# ------------ 3. 增删改查（天天写）------------
def user_demo():
    session = Session()
    try:
        # 增
        user = User(name="张三", age=25)
        session.add(user)
        session.commit()
        print(f"新增ID: {user.id}")

        # 查（工作中filter_by比filter常用）
        user = session.query(User).filter_by(name="张三").first()

        # 查（分页）
        users = (
            session.query(User)
            .filter(User.age > 18)
            .order_by(User.id.desc())
            .limit(20)
            .all()
        )

        # 改
        user.age = 26
        session.commit()

        # 删
        session.delete(user)
        session.commit()

    finally:
        session.close()


# ------------ 4. 真实项目模板（复制即用）------------
class UserService:
    """用户服务类"""

    def __init__(self):
        self.Session = Session

    def get_by_id(self, user_id):
        session = self.Session()
        try:
            return session.query(User).filter_by(id=user_id).first()
        finally:
            session.close()

    def get_list(self, page=1, page_size=20):
        session = self.Session()
        try:
            return (
                session.query(User)
                .order_by(User.id.desc())
                .offset((page - 1) * page_size)
                .limit(page_size)
                .all()
            )
        finally:
            session.close()

    def create(self, **kwargs):
        session = self.Session()
        try:
            user = User(**kwargs)
            session.add(user)
            session.commit()
            return user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update(self, user_id, **kwargs):
        session = self.Session()
        try:
            session.query(User).filter_by(id=user_id).update(kwargs)
            session.commit()
        finally:
            session.close()

    def delete(self, user_id):
        session = self.Session()
        try:
            session.query(User).filter_by(id=user_id).delete()
            session.commit()
        finally:
            session.close()


# ------------ 5. 初始化（真正的项目结构）------------
# config.py
DB_CONFIG = {
    "user": "root",
    "password": "123456",
    "host": "localhost",
    "port": 3306,
    "database": "test",
}


# db.py
def init_db():
    """初始化数据库连接"""
    url = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?charset=utf8mb4"
    engine = create_engine(url, pool_size=10, pool_pre_ping=True)
    Session = sessionmaker(bind=engine)
    return Session, engine


# models.py - 只定义表结构
Base = declarative_base()
# ... 定义你的模型

# services.py - 业务逻辑
# class UserService: ...
