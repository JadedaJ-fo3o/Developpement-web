from extensions import db
## Tables Users
class user(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

# Tables Regarde
class regarde(db.Model):
    id_regarde = db.Column(db.Integer, primary_key=True)
    name_serie = db.Column(db.String(80), nullable=False)
    rating_value = db.Column(db.String(80), nullable=False)
    # 这里是点击RegardButton后，存入API的原始ID
    external_id = db.Column(db.String(80)) 
    #  -- 存入图片的URL
    image_url = db.Column(db.String(255))
    # 外键
    id_user = db.Column(db.Integer, db.ForeignKey("user.id_user"), nullable=False)
    user = db.relationship('user', backref="regardes")

# Tables Avoir 
class avoir(db.Model):
    id_avoir = db.Column(db.Integer, primary_key=True)
    name_serie = db.Column(db.String(80), nullable=False)
    # 这里是点击AvoirButton后，存入API的原始ID
    external_id = db.Column(db.String(80))
    #  -- 存入图片的URL
    image_url = db.Column(db.String(255))
    # 外键
    id_user = db.Column(db.Integer, db.ForeignKey("user.id_user"), nullable=False)
    user = db.relationship('user', backref="avoirs")

