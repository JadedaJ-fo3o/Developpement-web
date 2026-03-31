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
            "summary": show.get("summary", "")
        })
    return shows