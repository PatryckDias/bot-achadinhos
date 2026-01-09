import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_amazon_price(url):
    response = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.select_one("#productTitle")
    price = soup.select_one(".a-price-whole")

    if not title or not price:
        return None

    title = title.get_text(strip=True)
    price = price.get_text(strip=True).replace(".", "").replace(",", ".")

    return {
        "title": title,
        "price": float(price),
        "url": url
    }
