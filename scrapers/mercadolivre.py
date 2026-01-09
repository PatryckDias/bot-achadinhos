import requests
import re
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
}


def get_ml_price(url): str) -> dict | None:
    """
    Busca título, preço atual e preço antigo (se existir)
    de um produto do Mercado Livre.
    """

    response = requests.get(url, headers=HEADERS, timeout=30)

    if response.status_code != 200:
        print(f"[Mercado Livre] HTTP {response.status_code}")
        return None

    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # ==============================
    # 🏷️ TÍTULO
    # ==============================
    title = None
    h1 = soup.find("h1")
    if h1:
        title = h1.get_text(strip=True)

    if not title:
        print("[Mercado Livre] Título não encontrado")
        return None

    # ==============================
    # 💰 PREÇO ATUAL
    # ==============================
    price = None

    # 1️⃣ Meta tag (mais confiável)
    meta_price = soup.find("meta", {"itemprop": "price"})
    if meta_price and meta_price.get("content"):
        try:
            price = float(meta_price["content"])
        except ValueError:
            pass

    # 2️⃣ JSON embutido
    if price is None:
        match = re.search(r'"price"\s*:\s*([0-9]+)', html)
        if match:
            price = float(match.group(1))

    # 3️⃣ Fallback visual
    if price is None:
        span_price = soup.select_one("span.andes-money-amount__fraction")
        if span_price:
            try:
                price = float(
                    span_price.text.replace(".", "").replace(",", ".")
                )
            except ValueError:
                pass

    if price is None:
        print("[Mercado Livre] Preço não encontrado")
        return None

    # ==============================
    # 💸 PREÇO ANTIGO (se existir)
    # ==============================
    old_price = None

    # Meta tag de preço original
    meta_old = soup.find("meta", {"itemprop": "originalPrice"})
    if meta_old and meta_old.get("content"):
        try:
            old_price = float(meta_old["content"])
        except ValueError:
            pass

    # Fallback visual
    if old_price is None:
        old_span = soup.select_one(
            "span.andes-money-amount--previous "
            "span.andes-money-amount__fraction"
        )
        if old_span:
            try:
                old_price = float(
                    old_span.text.replace(".", "").replace(",", ".")
                )
            except ValueError:
                pass

    # ==============================
    # 📦 RESULTADO FINAL
    # ==============================
    return {
        "site": "Mercado Livre",
        "title": title,
        "price": price,
        "old_price": old_price,
        "url": url,
    }
