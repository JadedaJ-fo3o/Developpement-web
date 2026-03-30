from flask import Blueprint, render_template, request, redirect, session, url_for
from extensions import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

# Register
@auth.route('/register', methods=['POST'])
def register():
    u = request.form.get('user')
    p = request.form.get('pass')
    # Check 逻辑
    user_exists = User.query.filter_by(username=u).first()
    if user_exists:
        return {"error": "Cet utilisateur existe déjà"}, 400
    # HASH 加密 -- PPT
    new_user = User(
        username=u, 
        password_hash=generate_password_hash(p)
    )
    db.session.add(new_user)
    db.session.commit()
    # 返回主页，在注册以后
    return redirect(url_for('auth.show_auth'))

# Log In
@auth.route('/login', methods=['POST'])
def login():
    u = request.form.get('user')
    p = request.form.get('pass')
    # 匹配 Users
    user = User.query.filter_by(username=u).first()
    if not user or not check_password_hash(user.password_hash, p):
        return {"error": "identifiants invalides"}, 401
    
    session["user_id"] = user.id_user #stock
    return redirect('/')

# Log out 
@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.show_auth'))


@auth.route('/auth')
def show_auth():
    return render_template('auth.html')