from flask import Flask
from commands import init_app
import config
from exts import db

app = Flask(__name__)
# 将 SQLAlchemy 实例与 Flask 应用关联
db.init_app(app)
app.config.from_object(config)
init_app(app)

if __name__ == "__main__":
    app.run()
