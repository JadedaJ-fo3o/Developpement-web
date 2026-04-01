from flask import Blueprint, g, jsonify, render_template, request
from models import Regarde
from routes.auth import login_required
from services.gemini import recommend_from_records

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
