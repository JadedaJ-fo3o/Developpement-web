from flask import Blueprint, render_template, request, redirect, session, url_for, g
from extensions import db
from models import User
from werkzeug.security import generate_password_hash
import functools

auth_bp = Blueprint('auth', __name__)

# login_required 装饰器
def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for('auth.show_auth'))
        g.user = User.get_by_username(session["user_id"])
        return f(*args, **kwargs)
    return decorated

# Register
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    u = data.get('user')
    p = data.get('pass')

    # Check 逻辑
    user_exists = User.get_by_username(u)
    if user_exists:
        return {"error": "Cet utilisateur existe déjà"}, 400

    # HASH 加密 -- PPT
    new_user = User(
        username=u,
        password_hash=generate_password_hash(p)
    )
    db.session.add(new_user)
    db.session.commit()

    # 注册成功 直接登录
    session["user_id"] = new_user.id_user
    return {"success": True}, 200

# Log In
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    u = data.get('user')
    p = data.get('pass')

    # 匹配 Users
    user = User.get_by_username(u)
    if not user or not user.check_password(p):
        return {"error": "Identifiants invalides"}, 401

    session["user_id"] = user.id_user  # stock
    return {"success": True}, 200

# Log out
@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.show_auth'))

@auth_bp.route('/auth')
def show_auth():
    return render_template('auth.html')