from flask import Blueprint, request, jsonify, render_template, g
from models import regarde, avoir
from routes.auth import login_required
from services.tvmaze import search_shows

series_bp = Blueprint('series', __name__)


@series_bp.route('/')
@login_required
def home():
    return render_template('series.html')


@series_bp.route('/api/search')
@login_required
def api_search():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])
    shows = search_shows(query)
    return jsonify(shows)


@series_bp.route('/add', methods=['POST'])
@login_required
def add_series():
    data = request.get_json()


@series_bp.route('/a-voir/add', methods=['POST'])
@login_required
def add_to_watchlist():
    data = request.get_json()



@series_bp.route('/rate', methods=['POST'])
@login_required
def rate():
    data = request.get_json()
