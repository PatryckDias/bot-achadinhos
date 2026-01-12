import os
from telegram import Bot
from scrapers.mercadolivre_api import get_ml_deals

# FORÇA leitura das variáveis
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

print("TOKEN:", TOKEN)
print("CHAT_ID:", CHAT_ID)

if not TOKEN:
    raise Exception("❌ TELEGRAM_TOKEN não encontrado no ambiente")
if not CHAT_ID:
    raise Exception("❌ TELEGRAM_CHAT_ID não encontrado no ambiente")

BOT = Bot(token=TOKEN)
