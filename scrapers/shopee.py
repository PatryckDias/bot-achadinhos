import requests
import json
import re

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9"
}

def get_shopee_price(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    html = r.text

    match = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
        html
    )

    if not match:
        print("❌ Shopee: __NEXT_DATA__ não encontrado")
        return None

    data = json.loads(match.group(1))

    try:
        page_props = data["props"]["pageProps"]

        # Tentativa 1 (mais comum)
        if "item" in page_props:
            product = page_props["item"]
        # Tentativa 2 (links SEO)
        elif "initialData" in page_props and "item" in page_props["initialData"]:
            product = page_props["initialData"]["item"]
        else:
            print("❌ Shopee: estrutura desconhecida")
            return None

        title = product["name"]
        price = product["price"] / 100000

    except Exception as e:
        print("❌ Shopee: erro ao extrair dados", e)
        return None

    return {
        "site": "Shopee",
        "title": title,
        "price": price,
        "url": url
    }
