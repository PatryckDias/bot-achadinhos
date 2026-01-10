import requests
import json
import re
from bs4 import BeautifulSoup
from pathlib import Path

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
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

    response = requests.get(category["url"], headers=HEADERS, timeout=30)
    if response.status_code != 200:
        return promos

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.select("li.ui-search-layout__item")

    for item in items:
        link = item.find("a", href=True)
        if not link:
            continue

        url = link["href"].split("#")[0]

        mlb_match = re.search(r"MLB\d+", url)
        if not mlb_match:
            continue

        mlb_id = mlb_match.group()

        if mlb_id in sent_cache:
            continue

        title_tag = item.find("h2")
        price_tag = item.select_one("span.andes-money-amount__fraction")

        if not title_tag or not price_tag:
            continue

        try:
            price = float(
                price_tag.text.replace(".", "").replace(",", ".")
            )
        except ValueError:
            continue

        if price > category["max_price"]:
            continue

        promos.append({
            "id": mlb_id,
            "title": title_tag.text.strip(),
            "price": price,
            "url": url,
            "category": category["name"]
        })

        sent_cache.add(mlb_id)

    save_cache(sent_cache)
    return promos
