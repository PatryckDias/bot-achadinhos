import requests
import json
from pathlib import Path

CACHE_FILE = Path("sent_cache.json")

API_URL = "https://api.mercadolibre.com/sites/MLB/search"


def load_cache():
    if CACHE_FILE.exists():
        return set(json.loads(CACHE_FILE.read_text()))
    return set()


def save_cache(cache):
    CACHE_FILE.write_text(json.dumps(list(cache)))


def get_promos_from_category(category):
    sent_cache = load_cache()
    promos = []

    params = {
        "q": category["query"],
        "sort": "price_asc",
        "limit": 20
    }

    response = requests.get(API_URL, params=params, timeout=30)
    if response.status_code != 200:
        print("[ML API] Erro HTTP", response.status_code)
        return promos

    data = response.json()
    results = data.get("results", [])

    print(f"[ML API] Resultados encontrados: {len(results)}")

    for item in results:
        mlb_id = item["id"]

        if mlb_id in sent_cache:
            continue

        price = item.get("price")
        original = item.get("original_price")

        if not price or not original:
            continue

        discount = int(100 - (price / original * 100))

        if discount < category["min_discount"]:
            continue

        promos.append({
            "id": mlb_id,
            "title": item["title"],
            "price": price,
            "old_price": original,
            "discount": discount,
            "url": item["permalink"],
            "category": category["name"]
        })

        sent_cache.add(mlb_id)

    save_cache(sent_cache)
    return promos
