import requests

def search_shopee(keyword, max_price):
    params = {
        "keyword": keyword,
        "limit": 20,
        "newest": 0,
        "order": "asc",
        "price_max": max_price
    }

    r = requests.get(
        "https://shopee.com.br/api/v4/search/search_items",
        params=params,
        timeout=15
    )

    if r.status_code != 200:
        return []

    items = r.json().get("items", [])
    results = []

    for i in items:
        item = i.get("item_basic")
        if not item:
            continue

        price = item["price"] / 100000
        if price <= max_price:
            results.append({
                "id": str(item["itemid"]),
                "title": item["name"],
                "price": price,
                "url": f"https://shopee.com.br/product/{item['shopid']}/{item['itemid']}"
            })

    return results
