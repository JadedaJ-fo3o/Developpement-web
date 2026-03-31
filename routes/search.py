from flask import Blueprint, request, jsonify, render_template
from routes.auth import login_required
from services.tvmaze import search_shows

series_bp = Blueprint('series', __name__)


@series_bp.route('/search')
@login_required
def search_test():
    return render_template('search.html')


@series_bp.route('/api/search')
@login_required
def api_search():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])
    shows = search_shows(query)
    return jsonify(shows)


