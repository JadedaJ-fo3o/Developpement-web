from flask import Flask, session, redirect, url_for
from extensions import db
from routes.auth import auth_bp
from routes.search import search_bp
from routes.home import home_bp
from routes.recommendations import recommendations_bp
from routes.listeseries import listeseries_bp
from routes.rating import rating_bp
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = "genflix_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
 ## ！！！非常重要！！
 # 加了一行数据库判断逻辑，判断数据库是否已经存在
    if not os.path.exists("database.db"):  #如果没有这行会直接新建db覆盖原数据！如果存在数据库，则不会新创建数据库，直接写入。
        db.create_all()

app.register_blueprint(auth_bp)
app.register_blueprint(search_bp)
app.register_blueprint(recommendations_bp)
app.register_blueprint(listeseries_bp)
app.register_blueprint(rating_bp)
app.register_blueprint(home_bp)


@app.route('/')
def home():
    if session.get("user"):
        return redirect(url_for("home.home_page"))
    return redirect(url_for("auth.show_auth"))

# @app.route('/home-test')
# def home_test():
#     return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=4000)