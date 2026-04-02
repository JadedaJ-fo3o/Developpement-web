import requests
from datetime import datetime

TVMAZE_BASE = "https://api.tvmaze.com"

def search_shows(query):
    try:
        response = requests.get(
            f"{TVMAZE_BASE}/search/shows",
            params={"q": query},
            timeout=8,
        )
    except requests.RequestException:
        return []

    if response.status_code != 200:
        return []
    results = response.json()
    shows = []
    for item in results:
        show = item["show"]
        shows.append({
            "id": show["id"],
            "url": show.get("url"),
            "name": show["name"],
            "type": show.get("type"),
            "language": show.get("language"),
            "genres": show.get("genres", []),
            "status": show.get("status"),
            "officialSite": show.get("officialSite"),
            "rating": show["rating"]["average"] if show.get("rating") else None,
            "image": show["image"]["medium"] if show.get("image") else None,
            "summary": show.get("summary", ""),
            "premiered": show.get("premiered") #添加了第一次上映时间
        })
    return shows



def get_top_rated_last_five_years(max_pages=200):
    current_year = datetime.now().year
    
    years = []
    for i in range(1, 6):
        years.append(current_year - i)

    best_by_year = {}
    for year in years:
        best_by_year[year] = None

    for page in range(max_pages):
        try:
            response = requests.get(
                f"{TVMAZE_BASE}/shows",
                params={"page": page}, 
                timeout=8,
            )
        except requests.RequestException:
            continue

        if response.status_code != 200:
            break

        rows = response.json() or []
        if not rows:
            break

        for show in rows:
            year = extract_year(show.get("premiered"))
            if year not in best_by_year:
                continue

            score = rating_score(show)
            current = best_by_year[year]
            current_score = rating_score(current) if current else -1
            if score > current_score:
                best_by_year[year] = show

    #sorted -> reperer
    items = []
    for year in sorted(best_by_year.keys(), reverse=True):
        show = best_by_year[year]
        if not show:
            continue
        items.append(to_item(show, reason=f"Meilleure note TVMaze en {year}."))
    return items

def to_item(show, reason=""):
    return {
        "id": show.get("id"),
        "url": show.get("url"),
        "name": show.get("name"),
        "type": show.get("type"),
        "language": show.get("language"),
        "genres": show.get("genres", []),
        "status": show.get("status"),
        "officialSite": show.get("officialSite"),
        "rating": (show.get("rating") or {}).get("average"),
        "image": (show.get("image") or {}).get("medium"),
        "summary": show.get("summary", ""),
        "premiered": show.get("premiered"),
        "reason": reason,
    }

def extract_year(date_text):
    if not date_text or len(date_text) < 4:
        return None
    try:
        return int(date_text[:4])
    except ValueError:
        return None


def rating_score(show):
    rating = (show.get("rating") or {}).get("average")
    if rating is None:
        return -1
    try:
        return float(rating)
    except (TypeError, ValueError):
        return -1


 ###########  返回 播放时间
def get_next_episode(show_id):
    try:
        resp = requests.get(
            f"{TVMAZE_BASE}/shows/{show_id}",
            params={"embed": "nextepisode"},
            timeout=8
        )
    except requests.RequestException:
        return {
            "next_airdate": None,
            "next_airtime": None,
            "next_ep_name": None
        }
    if resp.status_code != 200:
        return {
            "next_airdate": None,
            "next_airtime": None,
            "next_ep_name": None
        }
    data = resp.json()
    next_ep = data.get("_embedded", {}).get("nextepisode")
    return {
        "next_airdate": next_ep.get("airdate") if next_ep else None,
        "next_airtime": next_ep.get("airtime") if next_ep else None,
        "next_ep_name": next_ep.get("name") if next_ep else None
    }

