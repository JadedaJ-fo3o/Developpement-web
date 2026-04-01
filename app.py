from flask import Flask, render_template, session
from extensions import db
from routes.auth import auth_bp
from routes.search import search_bp
from routes.recommendations import recommendations_bp
from routes.listeseries import listeseries_bp
from routes.rating import rating_bp

app = Flask(__name__)

app.config["SECRET_KEY"] = "genflix_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)
app.register_blueprint(search_bp)
app.register_blueprint(recommendations_bp)
app.register_blueprint(listeseries_bp)
app.register_blueprint(rating_bp)


@app.route('/')
def home():
    username = session.get("user", None)
    if username is not None:
        return render_template("home.html")
    return render_template("auth.html")


@app.route('/home-test')
def home_test():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True, port=4000)