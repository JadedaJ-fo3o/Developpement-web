# Developpement-web
Projet sur le developpement web

# GenFlix — Structure du projet

## Architecture des fichiers
```
genflix/
├── app.py
├── extensions.py      # ← Initialisation: db = SQLAlchemy()
├── models.py          # ← Table => user, regarde, avoir, top
├── routes/
│   ├── auth.py
│   ├── search.py
│   ├── recommendations.py
│   └── listeseries.py   # Liste Regardé + A voir; Logique de notation (Note & Commentaires);
├── services/
│   ├── tvmaze.py
│   └── gemini.py
├── templates/
│   ├── home.html       # Page d'accueil => Classements annuels, publiés aujourd'hui, recommandations personnalisées (que 5 séries)
│   ├── auth.html
│   ├── search.html
│   ├── recommendations.html        # recommandations personnalisées (API Gemini)
│   ├── listeseries.html        # Liste Regardé + A voir
|   └── detaille.html       # Détailles du film, Histoire des commentaires
└── static/
    ├── css/style.css
    └── js/
        ├── auth.js
        ├── search.js
        ├── rating.js
        ├── recommendations.js
        └── listeseries.js      # Liste des vidéos vues + Liste des vidéos à voir + Logique de notation => Ajouter, modifier et supprimer des commentaires
