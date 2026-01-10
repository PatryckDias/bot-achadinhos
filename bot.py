import os
from telegram import Bot
from scrapers.mercadolivre_api import get_ml_deals

print("🔥 BOT EXECUTANDO 🔥")

BOT = Bot(os.getenv("TELEGRAM_TOKEN"))
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
getenv("TELEGRAM_CHAT_ID")

def run_bot():
    deals = get_ml_deals("ps5")

    print("[BOT] Ofertas encontradas:", len(deals))

def main():
    print("Buscando ofertas...")
    deals = get_ml_deals("ps5")
    print("Ofertas recebidas:", deals)

    for d in deals:
        msg = (
            f"🔥 *OFERTA MERCADO LIVRE*\n\n"
            f"{d['title']}\n\n"
            f"💰 De R$ {d['original']:.2f}\n"
            f"💥 Por R$ {d['price']:.2f}\n"
            f"📉 {d['discount']}% OFF\n\n"
            f"🛒 {d['url']}"
        )

        BOT.send_message(CHAT_ID, msg, parse_mode="Markdown")
        print("Mensagem enviada")

if __name__ == "__main__":
    print("🤖 Bot iniciado...")

    while True:
        try:
            run_bot()
        except Exception as e:
            print("Erro:", e)

        print("⏳ Aguardando 10 minutos...")
        time.sleep(300)   # 10 minutos
