import requests
import json
from pathlib import Path

API_URL = "https://api.mercadolibre.com/sites/MLB/search"
CACHE_FILE = Path("sent_cache.json")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.mercadolivre.com.br/",
    "Origin": "https://www.mercadolivre.com.br",
    "Connection": "keep-alive"
}



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
        "limit": 15
    }

    response = requests.get(
        API_URL,
        params=params,
        headers=HEADERS,
        timeout=30
    )

    if response.status_code != 200:
        print("[ML API] Erro HTTP:", response.status_code)
        return promos

    data = response.json()
    results = data.get("results", [])

    print(f"[ML API] Resultados encontrados: {len(results)}")

    for item in results:
        mlb_id = item.get("id")

        if not mlb_id or mlb_id in sent_cache:
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
    print(f"[ML API] Promos válidas: {len(promos)}")
    return promos
