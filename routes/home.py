from flask import Blueprint, jsonify, render_template, request
from routes.auth import login_required
from extensions import db
from models import Top
from models import Regarde
from sqlalchemy import func
from datetime import datetime, timedelta
import requests

home_bp = Blueprint("home", __name__)

# 从数据库读取打分和时间，HTML显示逻辑接入Jinja
def get_weekly_ranking():
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    results = (
        db.session.query(
            Regarde.external_id,
            Regarde.name_serie,
            func.avg(Regarde.rating_value).label("avg_rating")
        )
        .filter(Regarde.created_at >= one_week_ago)
        .group_by(Regarde.external_id, Regarde.name_serie)
        .order_by(func.avg(Regarde.rating_value).desc())
        .limit(5)
        .all()
    )
    ranking = []
    for external_id, name, avg_rating in results:
        ranking.append({
            "external_id": external_id,
            "name": name,
            "rating": round(avg_rating, 2)
        })
    return ranking

# 2025 的排行榜 // 从数据库来
def get_top10_2025():
    results = (
        db.session.query(
            Top.external_id,
            Top.name,
            Top.rating
        )
        .filter(Top.year == 2025)
        .order_by(Top.rank.asc())
        .limit(10)
        .all()
    )
    top_list = []
    for external_id, name, rating in results:
        top_list.append({
            "external_id": external_id,
            "name": name,
            "rating": round(rating, 2)
        })

    return top_list


# 今日在播
# 今日播出  - 导入tvmaze捕捉的
TVMAZE_BASE = "https://api.tvmaze.com"
def get_today_schedule(offset, limit):
    today = datetime.now().strftime("%Y-%m-%d")
    url = f"{TVMAZE_BASE}/schedule?date={today}"
    try:
        resp = requests.get(url, timeout=8)
    except requests.RequestException:
        return []
    if resp.status_code != 200:
        return []
    data = resp.json()
    sliced = data[offset : offset + limit]
    schedule = []
    for ep in sliced:
        show = ep.get("show", {})
        schedule.append({
            "show_id": show.get("id"),
            "name": show.get("name"),
            "episode": ep.get("name"),
            "airtime": ep.get("airtime"),
            "image": show["image"]["medium"] if show.get("image") else None
        })
    return schedule

@home_bp.route("/api/today-schedule")
def api_today_schedule():
    offset = request.args.get("offset", 0, type=int)
    limit = request.args.get("limit", 5, type=int)
    data = get_today_schedule(offset=offset, limit=limit)
    return jsonify(data)

# Recommandation

@home_bp.route("/home")
@login_required
def home_page():
    return render_template(
        "home.html",
        today_schedule = get_today_schedule(offset=0, limit=5),
        weekly_ranking = get_weekly_ranking(),
        top10_2025=get_top10_2025()
    )
