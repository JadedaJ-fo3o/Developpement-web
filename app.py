from flask import Flask, render_template, session
from extensions import db
from routes.auth import auth_bp
from routes.search import series_bp
from routes.recommendations import recommendations_bp
from routes.listeseries import listeseries_bp
from routes.rating import rating_bp

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
app.register_blueprint(series_bp)
app.register_blueprint(recommendations_bp)
app.register_blueprint(listeseries_bp)
app.register_blueprint(rating_bp)

# 根路由
@app.route('/')
def home():
    user_id = session.get("user_id", None)
    if user_id is not None:
        return render_template("home.html")
    return render_template("auth.html")

@app.route('/home-test')  # 仅测试用
def home_test():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True, port=4000)