# GRENADE 
Même dans les moments les plus sombres, l'écran continue de briller.

## Introduction
GRENADE, une plateforme permet à tous d'accéder à l'information et d'échanger des idées. Vous pouvez y consulter la programmation des séries du jour, la liste des séries populaires de la semaine, et rechercher des informations sur des œuvres spécifiques. Vous pouvez également enregistrer les programmes que vous avez vus et ceux à venir, et les noter et les commenter. Bien sûr, vous pouvez aussi lire les commentaires des autres utilisateurs.

Nous avons également conçu une fonction de recommandation basée sur l'IA, qui combine vos notes sur ce site avec les séries tendance en temps réel afin de générer intelligemment de nouvelles recommandations.

Les œuvres télévisuelles sont le reflet de différentes vies, avec leurs rires, leurs colères, leurs avidités, leurs haines et leurs illusions. 

# Structure du projet

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
```

## Guide d'installation

Pour utiliser l'API, vous devez créer un fichier `.env` :
```
GEMINI_API_KEY = "votre key api"
GEMINI_MODEL = gemini-2.0-flash
```
