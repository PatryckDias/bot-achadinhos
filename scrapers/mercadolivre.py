import requests

def search_ml(query, max_price):
    params = {
        "q": query,
        "limit": 20,
        "sort": "price_asc"
    }

    r = requests.get(
        "https://api.mercadolibre.com/sites/MLB/search",
        params=params,
        timeout=15
    )

    if r.status_code != 200:
        return []

    results = []
    for item in r.json().get("results", []):
        if item["price"] <= max_price:
            results.append({
                "id": item["id"],
                "title": item["title"],
                "price": item["price"],
                "url": item["permalink"]
            })
    return results
