# Developpement-web
Projet sur le developpement web

# GenFlix — Structure du projet

## Architecture des fichiers
```
genflix/
├── app.py
├── config.py
├── database.db
├── routes/
│   ├── auth.py
│   ├── series.py
│   ├── recommendations.py
│   └── watchlist.py
├── services/
│   ├── tvmaze.py
│   └── gemini.py
├── templates/
│   ├── base.html
│   ├── auth.html
│   ├── series.html
│   ├── recommendations.html
│   └── watchlist.html
└── static/
    ├── css/style.css
    └── js/
        ├── auth.js
        ├── search.js
        ├── rating.js
        └── recommendations.js
```

## Méthodes prévues

### `app.py`
```python
from flask import Flask
from config import SECRET_KEY, DATABASE
from routes.auth import auth_bp
from routes.series import series_bp
from routes.recommendations import recommendations_bp
from routes.watchlist import watchlist_bp
import sqlite3

def get_db(): ...
def init_db(): ...
def create_app(): ...

app = create_app()
if __name__ == "__main__":
    app.run(debug=True, port=4000)
```

### `config.py`
```python
SECRET_KEY = "genflix_secret_key"
DATABASE = "database.db"
GEMINI_API_KEY = "ta_clé_gemini_ici"
```

### `routes/auth.py`
```python
auth_bp = Blueprint('auth', __name__)

def login_required(f): ...          # décorateur — vérifie session, stocke g.user

@auth_bp.route('/login', methods=['GET', 'POST'])
def login(): ...

@auth_bp.route('/register', methods=['GET', 'POST'])
def register(): ...

@auth_bp.route('/logout')
def logout(): ...
```

### `routes/series.py`
```python
series_bp = Blueprint('series', __name__)

@series_bp.route('/')
@login_required
def home(): ...                     # affiche series.html + ratings de l'user

@series_bp.route('/api/search')
@login_required
def api_search(): ...               # GET ?q=... → JSON via TVmaze

@series_bp.route('/rate', methods=['POST'])
@login_required
def rate(): ...                     # enregistre sentiment en DB

@series_bp.route('/add', methods=['POST'])
@login_required
def add_series(): ...               # ajoute une série aux ratings
```

### `routes/recommendations.py`
```python
recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/recommandations')
@login_required
def recommendations_page(): ...     # affiche recommendations.html

@recommendations_bp.route('/api/recommandations')
@login_required
def api_recommendations(): ...      # appelle Gemini → JSON
```

### `routes/watchlist.py`
```python
watchlist_bp = Blueprint('watchlist', __name__)

@watchlist_bp.route('/a-voir')
@login_required
def watchlist_page(): ...           # affiche watchlist.html

@watchlist_bp.route('/a-voir/add', methods=['POST'])
@login_required
def add_to_watchlist(): ...         # ajoute en DB

@watchlist_bp.route('/a-voir/remove', methods=['POST'])
@login_required
def remove_watchlist(): ...         # supprime de la DB
```

### `services/tvmaze.py`
```python
def search_shows(query): ...        # appelle l'API TVmaze → liste de dicts
def get_show_info(show_id): ...     # retourne les détails d'une série
```

### `services/gemini.py`
```python
def analyze_profile(ratings_list): ...     # → texte profil utilisateur
def get_recommendations(profile_text): ... # → liste de noms de séries
```

### `static/js/search.js`
```javascript
async function searchShows(query) {}   // fetch GET /api/search?q=query
function displayResults(shows) {}      // génère les cards dans le DOM
```

### `static/js/rating.js`
```javascript
async function rateSeries(showId, sentiment) {}  // fetch POST /rate
function updateRatingUI(showId, sentiment) {}    // met à jour les boutons
```

### `static/js/recommendations.js`
```javascript
async function generateRecommendations() {}  // fetch GET /api/recommandations
function displayRecommendations(data) {}     // affiche profil + séries
```

### `static/js/auth.js`
```javascript
function validateForm() {}  // vérifie les champs login/register
```
