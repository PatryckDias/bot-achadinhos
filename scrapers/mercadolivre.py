import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9"
}

def get_ml_price(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    title = soup.select_one("h1.ui-pdp-title")
    price = soup.select_one("span.andes-money-amount__fraction")

    if not title or not price:
        print("❌ ML: título ou preço não encontrado")
        return None

    title = title.get_text(strip=True)
    price = price.get_text(strip=True).replace(".", "")

    try:
        price = float(price)
    except:
        print("❌ ML: erro ao converter preço")
        return None

    return {
        "site": "Mercado Livre",
        "title": title,
        "price": price,
        "url": url
    }
