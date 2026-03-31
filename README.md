# Developpement-web
Projet sur le developpement web

# GenFlix — Structure du projet

## Architecture des fichiers
```
genflix/
├── app.py
├── extensions.py      # ← 初始化 db = SQLAlchemy()
├── models.py          # ← user, regarde, avoir 三个类
├── routes/
│   ├── auth.py
│   ├── search.py
│   ├── recommendations.py
│   └── listeseries.py   # 已看+待看片单+打分逻辑 => 增加、修改和删除评论
├── services/
│   ├── tvmaze.py
│   └── gemini.py
├── templates/
│   ├── home.html       # 主页 => 2025年度榜单，本周放送，个性化推荐（Gemini API）
│   ├── auth.html
│   ├── search.html
│   ├── recommendations.html        # 个性化推荐
│   ├── listeseries.html        # 已看+待看片单
|   └── detaille.html       # 电影详情，打分+评价逻辑，展示评论
└── static/
    ├── css/style.css
    └── js/
        ├── auth.js
        ├── search.js
        ├── rating.js
        ├── recommendations.js
        └── listeseries.js      # 已看+待看片单+打分逻辑 => 增加、修改和删除评论
```
