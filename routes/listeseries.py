from flask import Blueprint, render_template, request, session, jsonify
from models import Regarde, Avoir, User
from routes.auth import login_required

listeseries_bp = Blueprint("listeseries", __name__)


# ===== 页面 =====
@listeseries_bp.route('/listeseries')
@login_required
def listeseries_test():
    return render_template('listeseries.html')


# ===== 工具：获取当前用户 =====
def get_user():
    username = session.get("user")
    if not username:
        return None
    return User.get_by_username(username)


# ===== 获取 watchlist =====
@listeseries_bp.route("/api/watchlist", methods=["GET"])
@login_required
def get_watchlist():

    user = get_user()
    if not user:
        return {"error": "not logged"}, 401

    user_id = user.id_user

    regardes = Regarde.query.filter_by(id_user=user_id).all()
    avoirs = Avoir.query.filter_by(id_user=user_id).all()

    return jsonify({
        "regardes": [
            {
                "external_id": r.external_id,
                "name_serie": r.name_serie,
                "image_url": r.image_url,
                "rating_value": r.rating_value,
                "commentaire": r.commentaire
            } for r in regardes
        ],
        "avoirs": [
            {
                "external_id": a.external_id,
                "name_serie": a.name_serie,
                "image_url": a.image_url
            } for a in avoirs
        ]
    })


# ===== AVOIR =====

# 👉 加入
@listeseries_bp.route("/api/avoir/add", methods=["POST"])
@login_required
def add_avoir():

    user = get_user()
    if not user:
        return {"error": "not logged"}, 401

    data = request.get_json()

    Avoir.add(
        user_id=user.id_user,
        external_id=data["external_id"],
        name_serie=data["name_serie"],
        image_url=data["image_url"]
    )

    return {"ok": True}


# 👉 删除
@listeseries_bp.route("/api/avoir/delete", methods=["POST"])
@login_required
def delete_avoir():

    user = get_user()
    if not user:
        return {"error": "not logged"}, 401

    data = request.get_json()

    Avoir.remove(user.id_user, data["external_id"])

    return {"ok": True}


# 👉 查询一个（给 detail 用）
@listeseries_bp.route("/api/avoir/get_one")
@login_required
def get_one_avoir():

    user = get_user()
    if not user:
        return {"error": "not logged"}, 401

    external_id = request.args.get("external_id")

    obj = Avoir.get_one(user.id_user, external_id)

    if not obj:
        return {}

    return {
        "external_id": obj.external_id
    }


# ===== REGARDE =====

# 👉 添加 / 更新评分
@listeseries_bp.route("/api/regarde/update", methods=["POST"])
@login_required
def update_regarde():

    user = get_user()
    if not user:
        return {"error": "not logged"}, 401

    data = request.get_json()

    Regarde.add_or_update(
        user_id=user.id_user,
        external_id=data["external_id"],
        name_serie=data["name_serie"],
        image_url=data["image_url"],
        rating_value=data["rating_value"],
        commentaire=data["commentaire"]
    )

    return {"ok": True}


# 👉 删除
@listeseries_bp.route("/api/regarde/delete", methods=["POST"])
@login_required
def delete_regarde():

    user = get_user()
    if not user:
        return {"error": "not logged"}, 401

    data = request.get_json()

    Regarde.remove(user.id_user, data["external_id"])

    return {"ok": True}


# 👉 查询一个（给 detail 回填）
@listeseries_bp.route("/api/regarde/get_one")
@login_required
def get_one_regarde():

    user = get_user()
    if not user:
        return {"error": "not logged"}, 401

    external_id = request.args.get("external_id")

    obj = Regarde.get_one(user.id_user, external_id)

    if not obj:
        return {}

    return {
        "external_id": obj.external_id,
        "rating_value": obj.rating_value,
        "commentaire": obj.commentaire
    }