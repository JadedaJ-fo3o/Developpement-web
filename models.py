from extensions import db
from werkzeug.security import check_password_hash
from datetime import datetime

## Tables Users
class User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # 验证密码
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 通过用户名查找用户
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

# Tables Regarde
class Regarde(db.Model):
    id_regarde = db.Column(db.Integer, primary_key=True)
    name_serie = db.Column(db.String(80), nullable=False)
    rating_value = db.Column(db.Integer, nullable=False)
    commentaire  = db.Column(db.Text, nullable=True) 
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)  # 时间戳的生成 - 逻辑取决于classmethode
    # 这里是点击RegardButton后，存入API的原始ID
    external_id = db.Column(db.String(80))
    #  -- 存入图片的URL
    image_url = db.Column(db.String(255))
    # 外键
    id_user = db.Column(db.Integer, db.ForeignKey("user.id_user"), nullable=False)
    user = db.relationship('User', backref="regardes")

    @classmethod
    def add_or_update(cls, user_id, external_id, name_serie, image_url, rating_value, commentaire):
        found = cls.get_one(user_id, external_id)

        if found:
            found.rating_value = rating_value
            found.commentaire = commentaire
            found.created_at = datetime.utcnow()
        else:
            found = cls(
                id_user=user_id,
                external_id=external_id,
                name_serie=name_serie,
                image_url=image_url,
                rating_value=rating_value,
                commentaire=commentaire
            )
            db.session.add(found)

        db.session.commit()

    @classmethod
    def get_one(cls, user_id, external_id):
        return cls.query.filter_by(id_user=user_id, external_id=external_id).first()

    @classmethod
    def remove(cls, user_id, external_id):
        found = cls.get_one(user_id, external_id)
        if found:
            db.session.delete(found)
            db.session.commit()
    @classmethod
    def get_by_serie(cls, external_id):
        return cls.query.filter_by(external_id=external_id)\
            .order_by(Regarde.created_at.desc())\
            .filter(Regarde.commentaire is not None).all()

# Tables Avoir
class Avoir(db.Model):
    id_avoir = db.Column(db.Integer, primary_key=True)
    name_serie = db.Column(db.String(80), nullable=False)
    # 这里是点击AvoirButton后，存入API的原始ID
    external_id = db.Column(db.String(80))
    #  -- 存入图片的URL
    image_url = db.Column(db.String(255))
    # 外键
    id_user = db.Column(db.Integer, db.ForeignKey("user.id_user"), nullable=False)
    user = db.relationship('User', backref="avoirs")

    # 通过用户ID获取 Avoir
    @classmethod
    def get_by_user(cls, user_id):
        return cls.query.filter_by(id_user=user_id).all()

    @classmethod
    def add(cls, user_id, external_id, name_serie, image_url):
        found = cls.get_one(user_id, external_id)
        if not found:
            obj = cls(
                id_user=user_id,
                external_id=external_id,
                name_serie=name_serie,
                image_url=image_url
            )
            db.session.add(obj)
            db.session.commit()
            
    @classmethod
    def get_one(cls, user_id, external_id):
        return cls.query.filter_by(id_user=user_id, external_id=external_id).first()

    @classmethod
    def remove(cls, user_id, external_id):
        found = cls.get_one(user_id, external_id)
        if found:
            db.session.delete(found)
            db.session.commit()


# Tables Top 10
class Top(db.Model):
    id_top = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.Integer, nullable=False)   # TVMaze show ID
    name = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(500), nullable=True)
    rank = db.Column(db.Integer, nullable=False)          # 1~10
    year = db.Column(db.Integer, nullable=False)          # e.g. 2025