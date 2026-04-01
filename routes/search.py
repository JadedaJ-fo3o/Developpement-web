from flask import Blueprint, request, jsonify, render_template
from routes.auth import login_required
from services.tvmaze import search_shows

search_bp = Blueprint('search', __name__)


@search_bp.route('/search')
@login_required
def search_test():
    return render_template('search.html')


@search_bp.route('/api/search')
@login_required
def api_search():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])
    shows = search_shows(query)
    return jsonify(shows)


