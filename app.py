from flask import Flask
from extensions import db,sess
from routes.auth import auth_bp
from routes.series import series_bp
from routes.recommendations import recommendations_bp
from routes.watchlist import watchlist_bp

def create_app():
    app = Flask(__name__)
    
    # 配置数据库
    app.config["SECRET_KEY"] = "genflix_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 初始化数据库
    db.init_app(app)
    sess.init_app(app)


    # 自动创建数据库和文件
    with app.app_context():
        db.create_all()

    # Register Blue Print
    app.register_blueprint(auth_bp)
    app.register_blueprint(series_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(watchlist_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=4000)