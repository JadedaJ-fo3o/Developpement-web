from flask import Blueprint, g, jsonify, render_template, request, session
import time
from models import Regarde, User
from routes.auth import login_required
from services.gemini import recommend_from_records
from services.tvmaze import get_top_rated_last_five_years

recommendations_bp = Blueprint('recommendations', __name__)
HOME_RECOMMENDATIONS_CACHE = {}
HOME_RECOMMENDATIONS_TTL_SECONDS = 600


def _records_signature(rows):
	return tuple(
		(row.name_serie or "", row.rating_value)
		for row in rows
	)




@recommendations_bp.route('/recommendations')
@login_required
def recommendation_test():
	return render_template('recommendations.html')

#用来调取recommendation的接口 Route API pour les recommandations 
@recommendations_bp.route('/api/recommendations', methods=['POST'])
@login_required
def recommendation_api():
	data = request.get_json(silent=True) or {}
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



@recommendations_bp.route('/api/home-recommendations', methods=['GET'])
def home_recommendations_api():
	fallback_items, fallback_message = _fallback_payload()

	username = session.get("user")
	if not username:
		return jsonify({
			"items": fallback_items,
			"mode": "fallback",
			"message": fallback_message,
		}), 200

	user = User.get_by_username(username)
	if user is None:
		return jsonify({
			"items": fallback_items,
			"mode": "fallback",
			"message": fallback_message,
		}), 200

	rows = Regarde.query.filter_by(id_user=user.id_user).all()
	if not rows:
		return jsonify({
			"items": fallback_items,
			"mode": "fallback",
			"message": fallback_message,
		}), 200

	records = []
	signature = _records_signature(rows)
	cache_key = (user.id_user, signature)
	cache_entry = HOME_RECOMMENDATIONS_CACHE.get(cache_key)
	if cache_entry and time.time() < cache_entry["expires_at"]:
		return jsonify(cache_entry["payload"]), 200

	for row in rows:
		records.append({
			'name_serie': row.name_serie,
			'rating_value': row.rating_value,
		})

	try:
		result = recommend_from_records(records, "Propose 5 séries TV adaptées à mes goûts.")
		items = list(result.get("items") or [])[:5]
	except Exception:
		items = []

	items = _dedupe_items(items) #déduplication - la série

	if len(items) < 5: #garantie d'avoir 5 recommandations
		fallback = _fallback_items()
		items.extend(fallback)
		items = _dedupe_items(items)

	payload = {
		"items": items[:5],
		"mode": "personalized",
		"message": "5 recommandations personnalisées par Gemini.",
	}
	HOME_RECOMMENDATIONS_CACHE[cache_key] = {
		"expires_at": time.time() + HOME_RECOMMENDATIONS_TTL_SECONDS,
		"payload": payload,
	}
	return jsonify(payload), 200

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


#local fallback
DEFAULT_FALLBACK_ITEMS = [
	{
		"id": None,
		"name": "Breaking Bad",
		"image": None,
		"rating": 9.5,
		"url": "https://www.tvmaze.com/shows/169/breaking-bad",
		"genres": ["Drama", "Crime", "Thriller"],
		"reason": "Classique fortement noté, apprécié par un large public.",
	},
	{
		"id": None,
		"name": "Chernobyl",
		"image": None,
		"rating": 9.3,
		"url": "https://www.tvmaze.com/shows/32315/chernobyl",
		"genres": ["Drama", "History"],
		"reason": "Mini-série saluée pour son écriture et sa réalisation.",
	},
	{
		"id": None,
		"name": "Dark",
		"image": None,
		"rating": 8.8,
		"url": "https://www.tvmaze.com/shows/20897/dark",
		"genres": ["Drama", "Science-Fiction", "Mystery"],
		"reason": "Intrigue dense et univers marquant.",
	},
	{
		"id": None,
		"name": "The Last of Us",
		"image": None,
		"rating": 8.9,
		"url": "https://www.tvmaze.com/shows/46562/the-last-of-us",
		"genres": ["Drama", "Action", "Horror"],
		"reason": "Série récente avec d'excellents retours critiques.",
	},
	{
		"id": None,
		"name": "Shogun",
		"image": None,
		"rating": 8.7,
		"url": "https://www.tvmaze.com/shows/61362/shogun",
		"genres": ["Drama", "History", "Adventure"],
		"reason": "Production récente, très bien notée et visuellement forte.",
	},
]

def _fallback_items():
	items = get_top_rated_last_five_years()[:5]
	if items:
		return items
	return DEFAULT_FALLBACK_ITEMS[:]


def _fallback_payload():
	items = get_top_rated_last_five_years()[:5]
	if items:
		return items, "Top séries des cinq dernières années (TVMaze)."
	return DEFAULT_FALLBACK_ITEMS[:], "TVMaze indisponible, recommandations locales de secours."