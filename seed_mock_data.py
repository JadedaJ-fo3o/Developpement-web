###加数据用，暂时没用 - 2026-03-31

from werkzeug.security import generate_password_hash

from app import app
from extensions import db
from models import User, Regarde, Avoir


def get_or_create_user(username: str, plain_password: str) -> User:
    user = User.get_by_username(username)
    if user is None:
        user = User(username=username, password_hash=generate_password_hash(plain_password))
        db.session.add(user)
        db.session.commit()
    return user


def upsert_regarde(user_id: int, external_id: str, name_serie: str, image_url: str, rating_value: str, commentaire: str):
    row = Regarde.get_one(user_id, external_id)
    if row is None:
        row = Regarde(
            id_user=user_id,
            external_id=external_id,
            name_serie=name_serie,
            image_url=image_url,
            rating_value=rating_value,
            commentaire=commentaire,
        )
        db.session.add(row)
    else:
        row.name_serie = name_serie
        row.image_url = image_url
        row.rating_value = rating_value
        row.commentaire = commentaire


def upsert_avoir(user_id: int, external_id: str, name_serie: str, image_url: str):
    row = Avoir.get_one(user_id, external_id)
    if row is None:
        row = Avoir(
            id_user=user_id,
            external_id=external_id,
            name_serie=name_serie,
            image_url=image_url,
        )
        db.session.add(row)
    else:
        row.name_serie = name_serie
        row.image_url = image_url


def seed():
    with app.app_context():
        db.create_all()

        user = get_or_create_user("demo", "demo123")

        regarde_items = [
            ("100", "Breaking Bad", "https://static.tvmaze.com/uploads/images/medium_portrait/0/2400.jpg", "aimé", "Excellent rythme et personnages."),
            ("200", "The Office", "https://static.tvmaze.com/uploads/images/medium_portrait/481/1204342.jpg", "neutre", "Sympa, mais pas toujours mon style."),
            ("300", "Riverdale", "https://static.tvmaze.com/uploads/images/medium_portrait/112/282648.jpg", "n'aime pas", "Je n'accroche pas au scénario."),
        ]

        avoir_items = [
            ("400", "Dark", "https://static.tvmaze.com/uploads/images/medium_portrait/163/407679.jpg"),
            ("500", "Severance", "https://static.tvmaze.com/uploads/images/medium_portrait/414/1035783.jpg"),
        ]

        for item in regarde_items:
            upsert_regarde(user.id_user, *item)

        for item in avoir_items:
            upsert_avoir(user.id_user, *item)

        db.session.commit()

        print("Seed terminé.")
        print("Compte test: username=demo, password=demo123")
        print(f"Regarde: {len(regarde_items)} lignes, Avoir: {len(avoir_items)} lignes")


if __name__ == "__main__":
    seed()
