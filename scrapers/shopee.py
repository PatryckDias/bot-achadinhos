import requests
import re

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def get_shopee_price(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    html = r.text

    title_match = re.search(r'"name":"(.*?)"', html)
    price_match = re.search(r'"price":(\d+)', html)

    if not title_match or not price_match:
        print("❌ Shopee: dados não encontrados")
        return None

    title = title_match.group(1)
    price = int(price_match.group(1)) / 100000

    return {
        "site": "Shopee",
        "title": title,
        "price": price,
        "url": url
    }
