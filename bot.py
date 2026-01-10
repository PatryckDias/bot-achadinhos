import time
from telegram import Bot
from config import *
from affiliates import *
from database import *
from scrapers.mercadolivre import search_ml
from scrapers.shopee import search_shopee

bot = Bot(token=TELEGRAM_TOKEN)

SEARCHES = [
    ("ps5 controle", 300),
    ("headset gamer", 250),
    ("ssd nvme", 400)
]

while True:
    for query, max_price in SEARCHES:

        for p in search_ml(query, max_price):
            if already_sent(p["id"]):
                continue

            url = ml_affiliate(p["url"], ML_AFFILIATE_ID)

            bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=f"🔥 *Oferta Mercado Livre*\n\n{p['title']}\n💰 R$ {p['price']:.2f}\n🔗 {url}",
                parse_mode="Markdown"
            )

            mark_sent(p["id"])
            time.sleep(5)

        for p in search_shopee(query, max_price):
            if already_sent(p["id"]):
                continue

            url = shopee_affiliate(p["url"], SHOPEE_AFFILIATE_ID)

            bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=f"🔥 *Oferta Shopee*\n\n{p['title']}\n💰 R$ {p['price']:.2f}\n🔗 {url}",
                parse_mode="Markdown"
            )

            mark_sent(p["id"])
            time.sleep(5)

    time.sleep(900)  # 15 minutos
