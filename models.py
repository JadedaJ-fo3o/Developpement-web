from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

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
    rating_value = db.Column(db.String(80), nullable=False)
    # 这里是点击RegardButton后，存入API的原始ID
    external_id = db.Column(db.String(80))
    #  -- 存入图片的URL
    image_url = db.Column(db.String(255))
    # 外键
    id_user = db.Column(db.Integer, db.ForeignKey("user.id_user"), nullable=False)
    user = db.relationship('User', backref="regardes")

    @classmethod
    def get_by_user(cls, user_id):
        return cls.query.filter_by(id_user=user_id).all()

    # 添加或更新评分
    @classmethod
    def add_or_update(cls, user_id, external_id, rating_value):
        found = cls.query.filter_by(id_user=user_id, external_id=external_id).first()
        if found:
            found.rating_value = rating_value
        else:
            found = cls(id_user=user_id, external_id=external_id, rating_value=rating_value)
            db.session.add(found)
        db.session.commit()

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

    # 添加到 Avoir
    @classmethod
    def add(cls, user_id, external_id, name_serie, image_url):
        found = cls(id_user=user_id, external_id=external_id, name_serie=name_serie, image_url=image_url)
        db.session.add(found)
        db.session.commit()

    # 从Avoir删除
    @classmethod
    def remove(cls, user_id, external_id):
        found = cls.query.filter_by(id_user=user_id, external_id=external_id).first()
        if found:
            db.session.delete(found)
            db.session.commit()