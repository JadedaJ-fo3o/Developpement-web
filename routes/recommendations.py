from flask import Blueprint, g, jsonify, render_template, request, session
from models import Regarde, User
from routes.auth import login_required
from services.gemini import recommend_from_records
from services.tvmaze import get_recent_running_show, get_top_rated_last_five_years

recommendations_bp = Blueprint('recommendations', __name__)


@recommendations_bp.route('/recommendations')
@login_required
def recommendation_test():
	return render_template('recommendations.html')

#用来调取recommendation的接口 Route API pour les recommandations 
@recommendations_bp.route('/api/recommendations', methods=['POST'])
@login_required
def recommendation_api():
	data = request.get_json() 
	user_question = (data.get('question') or '').strip()

	if not user_question:
		return jsonify({'error': 'Question vide'}), 400

	# 2) Charge l'historique
	rows = Regarde.query.filter_by(id_user=g.user.id_user).all()
	records = []
	for row in rows:
		records.append({
			'name_serie': row.name_serie,
			'rating_value': row.rating_value,
		})

	# 3) la recommendation
	try:
		result = recommend_from_records(records, user_question)
		return jsonify(result), 200
	except Exception as exc:
		error_message = f'Erreur lors de la génération des recommandations: {str(exc)}'
		return jsonify({'items': [], 'message': error_message}), 500 


def _fallback_items():
	return get_top_rated_last_five_years()[:5]




@recommendations_bp.route('/api/home-recommendations', methods=['GET'])
def home_recommendations_api():
	username = session.get("user")
	if not username:
		return jsonify({
			"items": _fallback_items(),
			"mode": "fallback",
			"message": "Top séries des cinq dernières années (TVMaze).",
		}), 200

	user = User.get_by_username(username)
	if user is None:
		return jsonify({
			"items": _fallback_items(),
			"mode": "fallback",
			"message": "Top séries des cinq dernières années (TVMaze).",
		}), 200

	rows = Regarde.query.filter_by(id_user=user.id_user).all()
	if not rows:
		return jsonify({
			"items": _fallback_items(),
			"mode": "fallback",
			"message": "Top séries des cinq dernières années (TVMaze).",
		}), 200

	records = []
	for row in rows:
		records.append({
			'name_serie': row.name_serie,
			'rating_value': row.rating_value,
		})

	try:
		result = recommend_from_records(records, "Propose 4 séries TV adaptées à mes goûts.")##add prompt
		items = list(result.get("items") or [])[:4]
	except Exception:
		items = []

	exclude_ids = [item.get("id") for item in items if item.get("id") is not None]
	recent = get_recent_running_show(exclude_ids=exclude_ids)
	if recent:
		items.append(recent)

	items = _dedupe_items(items) #déduplication - la série

	if len(items) < 5: #garantie d'avoir 5 recommandations
		fallback = _fallback_items()
		items.extend(fallback)
		items = _dedupe_items(items)

	return jsonify({
		"items": items[:5],
		"mode": "personalized",
		"message": "4 recommandations personnalisées + 1 série récente en cours.",
	}), 200

#déduplication
def _dedupe_items(items):
	seen = set()
	clean = []
	for item in items:
		item_id = item.get("id")
		name = (item.get("name") or "").strip().lower()
		key = f"id:{item_id}" if item_id is not None else f"name:{name}"
		if key in seen:
			continue
		seen.add(key)
		clean.append(item)
	return clean

