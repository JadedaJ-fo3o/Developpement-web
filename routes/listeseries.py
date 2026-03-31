from flask import Blueprint, render_template, request, session, jsonify
from models import Regarde, Avoir, User
from routes.auth import login_required

listeseries_bp = Blueprint("listeseries", __name__)

@listeseries_bp.route('/listeseries')
@login_required
def listeseries_test():
    return render_template('listeseries.html')

# 👉 获取 watchlist
@listeseries_bp.route("/api/watchlist", methods=["GET"])
def get_watchlist():
    username = session.get("user")
    user = User.get_by_username(username)

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


# 加入 avoir
@listeseries_bp.route("/api/avoir/add", methods=["POST"])
def add_avoir():
    data = request.get_json()
    username = session.get("user")
    user = User.get_by_username(username)

    user_id = user.id_user

    Avoir.add(
        user_id=user_id,
        external_id=data["external_id"],
        name_serie=data["name_serie"],
        image_url=data["image_url"]
    )

    return {"ok": True}

# 删除
@listeseries_bp.route("/api/avoir/delete", methods=["POST"])
def delete_avoir():
    data = request.get_json()
    username = session.get("user")
    user = User.get_by_username(username)

    user_id = user.id_user

    Avoir.remove(user_id, data["external_id"])

    return {"ok": True}


# 加入 regarde（= 从 avoir 移过去）
@listeseries_bp.route("/api/regarde/add", methods=["POST"])
def add_regarde():
    data = request.get_json()
    username = session.get("user")
    user = User.get_by_username(username)

    user_id = user.id_user

    # 删除 avoir
    Avoir.remove(user_id, data["external_id"])

    # 加入 regarde
    Regarde.add_or_update(
        user_id=user_id,
        external_id=data["external_id"],
        name_serie=data["name_serie"],
        image_url=data["image_url"],
        rating_value=data.get("rating_value", "3"),
        commentaire=data.get("commentaire", "")
    )

    return {"ok": True}


# 修改评分 / 评论
@listeseries_bp.route("/api/regarde/update", methods=["POST"])
def update_regarde():
    data = request.get_json()
    username = session.get("user")
    user = User.get_by_username(username)

    user_id = user.id_user

    Regarde.add_or_update(
        user_id=user_id,
        external_id=data["external_id"],
        name_serie=data["name_serie"],
        image_url=data["image_url"],
        rating_value=data["rating_value"],
        commentaire=data["commentaire"]
    )

    return {"ok": True}


# 删除
@listeseries_bp.route("/api/regarde/delete", methods=["POST"])
def delete_regarde():
    data = request.get_json()
    username = session.get("user")
    user = User.get_by_username(username)

    user_id = user.id_user

    Regarde.remove(user_id, data["external_id"])

    return {"ok": True}

