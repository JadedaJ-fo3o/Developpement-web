from flask import Blueprint, request, jsonify, render_template
import requests as req
from routes.auth import login_required
from services.tvmaze import search_shows
from models import Regarde

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

@search_bp.route('/detail')
@login_required
def detail():
    show_id = request.args.get('id')
    return render_template('detaille.html', show_id=show_id)


@search_bp.route('/api/detail/<int:show_id>')
@login_required
def api_detail(show_id):
    show_resp = req.get(f"https://api.tvmaze.com/shows/{show_id}?embed[]=cast&embed[]=crew")
    akas_resp = req.get(f"https://api.tvmaze.com/shows/{show_id}/akas")
   
    if show_resp.status_code != 200:
        return jsonify({"error": "Show not found"}), 404
   
    show = show_resp.json()
    akas = akas_resp.json() if akas_resp.status_code == 200 else []

    cast = []
    for item in show.get('_embedded', {}).get('cast', [])[:10]:
        cast.append({
            "name": item['person']['name'],
            "character": item['character']['name'],
            "image": item['person']['image']['medium'] if item['person'].get('image') else None
        })

    directors = []
    writers = []
    for item in show.get('_embedded', {}).get('crew', []):
        ctype = item.get('type', '')
        name = item['person']['name']
        if 'Director' in ctype or 'Creator' in ctype:
            directors.append(name)
        elif 'Writer' in ctype:
            writers.append(name)
   
    aka_names = [a['name'] for a in akas if a.get('name')]
   
    network = show.get('network') or show.get('webChannel') or {}
    country = network.get('country', {}) or {}
   
    result = {
        "id": show['id'],
        "name": show['name'],
        "url": show.get('url'),
        "type": show.get('type'),
        "language": show.get('language'),
        "genres": show.get('genres', []),
        "status": show.get('status'),
        "premiered": show.get('premiered'),
        "runtime": show.get('runtime') or show.get('averageRuntime'),
        "country": country.get('name'),
        "rating": show['rating']['average'] if show.get('rating') else None,
        "image": show['image']['original'] if show.get('image') else None,
        "summary": show.get('summary', ''),
        "directors": directors,
        "writers": writers,
        "cast": cast,
        "akas": aka_names,
    }
    return jsonify(result)

@search_bp.route('/api/detail/<int:show_id>/comment', methods=['GET'])
@login_required
def get_comment(show_id):
    histoire = Regarde.get_by_serie(str(show_id))
    if histoire is None:
        return {"error": "History not found"}, 404
    
    comments = []
    for item in histoire:
        if item.commentaire:
            comments.append({
                "commentaire": item.commentaire,
                "created_at": item.created_at.isoformat()
            })

    return jsonify(comments)
