import requests
import os

ML_AFFILIATE_ID = os.getenv("ML_AFFILIATE_ID")

BASE_URL = "https://api.mercadolibre.com/sites/MLB/search"

def get_ml_deals(query):
    params = {
        "q": query,
        "limit": 10,
        "sort": "price_asc"
    }

    r = requests.get(BASE_URL, params=params, timeout=20)

    if r.status_code != 200:
        print("[ML] API error:", r.status_code)
        return []

    data = r.json()
    deals = []

    for item in data.get("results", []):
        price = item["price"]
        original = item.get("original_price")

        if not original:
            continue

        discount = int((1 - price / original) * 100)

        if discount < 25:
            continue

        affiliate_url = (
            item["permalink"]
            + f"?matt_tool=123&matt_campaign=ML_AFFILIATE&matt_affiliate={ML_AFFILIATE_ID}"
        )

        deals.append({
            "title": item["title"],
            "price": price,
            "original": original,
            "discount": discount,
            "url": affiliate_url
        })

    return deals
