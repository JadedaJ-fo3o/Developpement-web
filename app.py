from flask import Flask, session, redirect, url_for
from extensions import db
from routes.auth import auth_bp
from routes.search import search_bp
from routes.home import home_bp
from routes.recommendations import recommendations_bp
from routes.listeseries import listeseries_bp
from routes.rating import rating_bp
from models import Top
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = "genflix_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    # Verifier si la base de données existe déjà avant de la créer
    if not os.path.exists("database.db"):  # Si le fichier de base de données n'existe pas, créez-le
        db.create_all()

    if Top.query.count() == 0:
        top10_data = [
            {"external_id": 169,  "name": "Breaking Bad",    "rating": 4.9, "image": "https://static.tvmaze.com/uploads/images/medium_portrait/501/1253519.jpg", "rank": 1,  "year": 2025},
            {"external_id": 82,   "name": "Game of Thrones", "rating": 4.8, "image": "https://static.tvmaze.com/uploads/images/medium_portrait/498/1245274.jpg",  "rank": 2,  "year": 2025},
            {"external_id": 431,  "name": "Sherlock",         "rating": 4.8, "image": "https://static.tvmaze.com/uploads/images/medium_portrait/171/428042.jpg",   "rank": 3,  "year": 2025},
            {"external_id": 2993, "name": "Stranger Things",  "rating": 4.7, "image": "https://static.tvmaze.com/uploads/images/medium_portrait/595/1489169.jpg",  "rank": 4,  "year": 2025},
            {"external_id": 1955, "name": "Dark",             "rating": 4.7, "image": "https://static.tvmaze.com/uploads/images/medium_portrait/504/1262352.jpg",  "rank": 5,  "year": 2025},
            {"external_id": 66,   "name": "The Walking Dead", "rating": 4.6, "image": "https://static.tvmaze.com/uploads/images/medium_portrait/0/2400.jpg",       "rank": 6,  "year": 2025},
            {"external_id": 216,  "name": "Vikings",          "rating": 4.6, "image": "https://static.tvmaze.com/uploads/images/medium_portrait/160/401704.jpg",   "rank": 7,  "year": 2025},
            {"external_id": 13,   "name": "The Flash",        "rating": 4.5, "image": "https://static.tvmaze.com/uploads/images/medium_portrait/200/501943.jpg",   "rank": 8,  "year": 2025},
            {"external_id": 24,   "name": "Arrow",            "rating": 4.5, "image": "https://static.tvmaze.com/uploads/images/medium_portrait/160/401705.jpg",   "rank": 9,  "year": 2025},
            {"external_id": 12,  "name": "Supernatural",     "rating": 4.5, "image": "https://static.tvmaze.com/uploads/images/medium_portrait/445/1114097.jpg",  "rank": 10, "year": 2025},
        ]
        items = [Top(**data) for data in top10_data]
        db.session.add_all(items)
        db.session.commit()
        print("Top10 Data inserted into the database.")

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