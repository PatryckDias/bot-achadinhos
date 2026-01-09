import os
from telegram import Bot

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        raise Exception("Variáveis de ambiente não encontradas")

    bot = Bot(token=token)

    mensagem = (
        "🤖 Bot de Achadinhos ONLINE!\n\n"
        "✅ GitHub Actions funcionando\n"
        "✅ Telegram conectado\n"
        "🚀 Próximo passo: buscar ofertas automaticamente"
    )

    bot.send_message(chat_id=chat_id, text=mensagem)

if __name__ == "__main__":
    main()
