from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# 1. 连接数据库（把root/123456改成你的）
# 格式: mysql+pymysql://用户名:密码@地址/数据库名
engine = create_engine("mysql+pymysql://root:123456@localhost/test")

# 2. 创建会话类（用它操作数据库）
Session = sessionmaker(bind=engine)

# 3. 基类（所有表都要继承它）
Base = declarative_base()


# 4. 定义表结构（像写Python类一样）
class User(Base):
    __tablename__ = "users"  # 表名
    id = Column(Integer, primary_key=True)  # 主键自增
    name = Column(String(50))  # 用户名
    age = Column(Integer)  # 年龄


# 5. 建表（运行一次就会创建表）
Base.metadata.create_all(engine)


# 6. 自动管理session（不用手动关连接）
@contextmanager
def get_session():
    session = Session()
    try:
        yield session  # 返回session给你用
        session.commit()  # 没报错就提交
    except:
        session.rollback()  # 报错就回滚
        raise
    finally:
        session.close()  # 最后关闭连接


# 7. 增删改查（天天写）
# 增：添加用户
with get_session() as session:
    user = User(name="张三", age=25)  # 创建用户对象
    session.add(user)  # 添加到数据库
    # 提交后user.id自动有值

# 查：查询单个用户
with get_session() as session:
    user = session.query(User).filter_by(name="张三").first()
    # first()拿第一个，找不到返回None

# 查：查询列表（分页）
with get_session() as session:
    users = session.query(User).filter(User.age > 18).limit(10).all()
    # all()返回所有符合条件的

# 改：修改用户
with get_session() as session:
    user = session.query(User).filter_by(name="张三").first()
    if user:  # 找到了才改
        user.age = 26  # 直接改属性

# 删：删除用户
with get_session() as session:
    user = session.query(User).filter_by(name="张三").first()
    if user:
        session.delete(user)  # 删除这个用户


# 8. 封装成服务（实际项目这么写）
class UserService:
    # 查单个
    def get(self, id):
        with get_session() as s:
            return s.query(User).filter_by(id=id).first()

    # 查列表（分页）
    def list(self, page=1, size=10):
        with get_session() as s:
            return s.query(User).offset((page - 1) * size).limit(size).all()

    # 新增
    def create(self, **kwargs):
        with get_session() as s:
            user = User(**kwargs)  # 传name=张三, age=25
            s.add(user)
            return user  # 返回带id的用户对象

    # 修改
    def update(self, id, **kwargs):
        with get_session() as s:
            s.query(User).filter_by(id=id).update(kwargs)

    # 删除
    def delete(self, id):
        with get_session() as s:
            s.query(User).filter_by(id=id).delete()


# 9. 使用示例
service = UserService()

# 增
user = service.create(name="李四", age=30)
print(user.id)  # 打印新增用户的ID

# 查
user = service.get(1)
print(user.name, user.age)  # 打印用户信息

# 改
service.update(1, age=31)  # 把ID=1的用户年龄改成31

# 删
service.delete(1)  # 删除ID=1的用户

"""
重点：
1. 定义表：class User(Base)
2. 查询：session.query(表).filter_by(条件).first()
3. 增删改：add/delete后自动提交
"""
