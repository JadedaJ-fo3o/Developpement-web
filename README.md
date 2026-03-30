# Developpement-web
Projet sur le developpement web
Structure:
genflix/
│
├── app.py                  # Point d'entrée + init DB
├── config.py               # Clés API (TVmaze, Gemini)
│
├── routes/
│   ├── __init__.py
│   ├── auth.py             # /login, /register, /logout
│   ├── series.py           # / (home+search), /rate, /add
│   ├── recommendations.py  # /recommandations (Gemini)
│   └── watchlist.py        # /a-voir (liste "à voir")
│
├── services/
│   ├── tvmaze.py           # search(query) → liste de séries
│   └── gemini.py           # analyze_profile(series_list) → texte
│                           # get_recommendations(profil) → séries
│
├── templates/
│   ├── base.html           # Layout + navbar
│   ├── auth.html           # login + inscrire
│   ├── series.html         # Home : recherche + "Mes séries annotées"
│   ├── recommendations.html# Profil Gemini + bouton générer
│   └── watchlist.html      # Page "A voir"
│
├── static/
│   └── style.css
│
└── database.db             # SQLite — users, ratings, watchlist