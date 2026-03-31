from flask import Flask, render_template, session, redirect, url_for
from extensions import db
from routes.auth import auth_bp
from models import User

def create_app():
    app = Flask(__name__)

    # 配置数据库
    app.config["SECRET_KEY"] = "genflix_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 初始化数据库
    db.init_app(app)

    # 自动创建数据库和文件
    with app.app_context():
        db.create_all()

    # 注册 Blueprint
    app.register_blueprint(auth_bp)

    # 根路由
    @app.route('/')
    def home():
        username = session.get("user", None)
        if username is not None:
            return render_template("app.html")
        return render_template("auth.html") ## 后续需要改路径

    # 个人页面
    @app.route('/dashboard')
    def dashboard():
        username = session.get("user", None)
        if username is not None:
            return render_template("dashboard.html", user=User.get_by_username(username))
        return redirect(url_for('home'))

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=4000)