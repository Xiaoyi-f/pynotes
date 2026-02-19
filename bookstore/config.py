import os

DEBUG = True
SQLALCHEMY_DATABASE_URL = "sqlite://db/database.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭 SQLAlchemy 的修改跟踪，节省内存
SQLALCHEMY_ECHO = True  # SQLALCHEMY_ECHO：开启 SQL 语句日志输出，方便调试
SECRET_KEY = os.urandom(24)  # 生成24个字节的随机数据
