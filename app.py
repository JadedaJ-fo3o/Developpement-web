# 只导入了flask
from flask import Flask, session 
from extensions import db,sess
from models import user,regarde,avoir  # 导入数据库中的Tables

# Copy TD2
app = Flask(__name__)

# 配置数据库
app.config["SECRET_KEY"] = "dev-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Sapp.config["SESSION_TYPE"] = "sqlalchemy"
app.config["SESSION_TYPE"] = "sqlalchemy"
app.config["SESSION_SQLALCHEMY"] = db

# 初始化 sess 和 db
db.init_app(app)
sess.init_app(app)

# 自动创建数据库和文件
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)