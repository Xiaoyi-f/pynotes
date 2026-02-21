from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# 避免依赖循环导入，否则python解析不了
