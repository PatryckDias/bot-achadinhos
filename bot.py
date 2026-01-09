import os
from telegram import Bot
from products import PRODUCTS
from scrapers.mercadolivre import get_ml_price

def main():
    bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    for product in PRODUCTS:
        if product["site"] == "mercadolivre":
            data = get_ml_price(product["url"])

            if not data:
                continue

            msg = (
                f"🔥 *Oferta Mercado Livre*\n\n"
                f"{data['title']}\n\n"
                f"💰 Preço: R$ {data['price']:.2f}\n"
                f"🔗 {data['url']}"
            )

            bot.send_message(
                chat_id=chat_id,
                text=msg,
                parse_mode="Markdown"
            )

if __name__ == "__main__":
    main()
