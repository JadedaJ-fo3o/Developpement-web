import requests
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


def _extract_year(date_text):
    if not date_text or len(date_text) < 4:
        return None
    try:
        return int(date_text[:4])
    except ValueError:
        return None


def _rating_score(show):
    rating = (show.get("rating") or {}).get("average")
    if rating is None:
        return -1
    try:
        return float(rating)
    except (TypeError, ValueError):
        return -1


def _to_item(show, reason=""):
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


def get_top_rated_last_five_years(max_pages=200):
    from datetime import datetime

    current_year = datetime.utcnow().year
    # Use the last 5 completed years to avoid sparse data at the beginning of a new year.
    years = [current_year - i for i in range(1, 6)]
    best_by_year = {year: None for year in years}

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
            year = _extract_year(show.get("premiered"))
            if year not in best_by_year:
                continue

            score = _rating_score(show)
            current = best_by_year[year]
            current_score = _rating_score(current) if current else -1
            if score > current_score:
                best_by_year[year] = show

    items = []
    for year in sorted(best_by_year.keys(), reverse=True):
        show = best_by_year[year]
        if not show:
            continue
        items.append(_to_item(show, reason=f"Meilleure note TVMaze en {year}."))
    return items


def get_recent_running_show(exclude_ids=None, max_pages=20):
    excluded = set(exclude_ids or [])
    best_show = None
    best_key = (-1, -1)  # (year, rating)

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
            show_id = show.get("id")
            if show_id in excluded:
                continue
            if show.get("status") != "Running":
                continue

            year = _extract_year(show.get("premiered")) or -1
            score = _rating_score(show)
            key = (year, score)
            if key > best_key:
                best_key = key
                best_show = show

    if not best_show:
        return None
    return _to_item(best_show, reason="Série récente en cours de diffusion.")

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

