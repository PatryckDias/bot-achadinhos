import os
import requests
from products import PRODUCTS
from scrapers.mercadolivre import get_ml_price


def send_telegram_message(text):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }

    r = requests.post(url, json=payload)
    print("Telegram status:", r.status_code, r.text)


def main():
    for product in PRODUCTS:
        if product["site"] == "mercadolivre":
            data = get_ml_price(product["url"])

            print("DEBUG DATA:", data)

            if not data:
                continue

            msg = (
                f"🔥 *Oferta Mercado Livre*\n\n"
                f"{data['title']}\n\n"
                f"💰 Preço: R$ {data['price']:.2f}\n"
                f"🔗 {data['url']}"
            )

            send_telegram_message(msg)


if __name__ == "__main__":
    main()
