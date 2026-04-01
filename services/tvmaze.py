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

