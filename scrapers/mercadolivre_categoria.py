import requests
import json
import re
from bs4 import BeautifulSoup
from pathlib import Path

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
    "Accept-Language": "pt-BR,pt;q=0.9"
}

CACHE_FILE = Path("sent_cache.json")


def load_cache():
    if CACHE_FILE.exists():
        return set(json.loads(CACHE_FILE.read_text()))
    return set()


def save_cache(cache):
    CACHE_FILE.write_text(json.dumps(list(cache)))


def get_promos_from_category(category):
    sent_cache = load_cache()
    promos = []

    print(f"[ML MOBILE] Acessando: {category['url']}")

    response = requests.get(
        category["url"],
        headers=HEADERS,
        timeout=30
    )

    if response.status_code != 200:
        print(f"[ML MOBILE] Erro HTTP: {response.status_code}")
        return promos

    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.select("a.ui-search-item__group__element")

    print(f"[ML MOBILE] Itens encontrados: {len(items)}")

    for item in items:
        url = item.get("href")
        if not url:
            continue

        mlb_match = re.search(r"MLB\d+", url)
        if not mlb_match:
            continue

        mlb_id = mlb_match.group()

        if mlb_id in sent_cache:
            continue

        title = item.select_one("h2")
        price = item.select_one("span.price-tag-fraction")

        if not title or not price:
            continue

        try:
            value = float(price.text.replace(".", "").replace(",", "."))
        except:
            continue

        if value > category["max_price"]:
            continue

        promos.append({
            "id": mlb_id,
            "title": title.text.strip(),
            "price": value,
            "url": url,
            "category": category["name"]
        })

        sent_cache.add(mlb_id)

    save_cache(sent_cache)
    print(f"[ML MOBILE] Promos válidas: {len(promos)}")

    return promos
