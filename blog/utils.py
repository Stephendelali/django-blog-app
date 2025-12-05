import requests

def fetch_devto_articles(username=None, tag=None, per_page=6):
    """
    Fetch articles from Dev.to API.
    You can filter by username or tag if you want.
    """
    url = "https://dev.to/api/articles"
    params = {
        "per_page": per_page
    }
    if username:
        params["username"] = username
    if tag:
        params["tag"] = tag

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("Error fetching Dev.to articles:", e)
        return []
