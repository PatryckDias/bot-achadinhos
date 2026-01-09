def parse_price_mercadolivre(soup, html):
    # 1️⃣ Tenta meta tag (mais confiável)
    meta = soup.find("meta", {"itemprop": "price"})
    if meta and meta.get("content"):
        return float(meta["content"])

    # 2️⃣ Tenta JSON embutido
    import re
    match = re.search(r'"price"\s*:\s*([0-9]+)', html)
    if match:
        return float(match.group(1))

    # 3️⃣ Fallback visual (menos confiável)
    span = soup.select_one("span.andes-money-amount__fraction")
    if span:
        return float(span.text.replace(".", "").replace(",", "."))

    return None
