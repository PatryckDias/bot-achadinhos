import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def get_promos_from_search(category):
    params = {
        "q": category["query"],
        "limit": 10,
        "sort": "price_asc"
    }

    r = requests.get(
        "https://api.mercadolibre.com/sites/MLB/search",
        headers=HEADERS,
        params=params,
        timeout=20
    )

    if r.status_code != 200:
        print(f"[ML API] Erro HTTP: {r.status_code}")
        return []

    data = r.json()
    promos = []

    for item in data.get("results", []):
        price = item.get("price", 0)

        if price > category["max_price"]:
            continue

        promos.append({
            "id": item["id"],
            "title": item["title"],
            "price": price,
            "url": item["permalink"],
            "category": category["name"]
        })

    return promos
