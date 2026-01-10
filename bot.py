import os
from telegram import Bot
from categories import CATEGORIES
from scrapers.mercadolivre_categoria import get_promos_from_category

def main():
    bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    for category in CATEGORIES:
        print(f"[BOT] Buscando categoria: {category['name']}")
        promos = get_promos_from_category(category)
        print(f"[BOT] Promos retornadas: {len(promos)}")


        for p in promos:
            msg = (
                f"🔥 *PROMOÇÃO – {p['category']}*\n\n"
                f"{p['title']}\n\n"
                f"💰 *R$ {p['price']:.2f}*\n"
                f"🔗 {p['url']}"
            )

            bot.send_message(
                chat_id=chat_id,
                text=msg,
                parse_mode="Markdown"
            )

if __name__ == "__main__":
    main()
