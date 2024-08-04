from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from gemini_llm import generator

TOKEN: Final = 'Private_TOKEN'
BOT_USERNAME: Final = '@private_user_name'
YOUR_TELEGRAM_API = 'Your_Private_telegram_API'

async def handle_response(text: str, update: Update) -> str:
    if str(update.message.chat.id) == YOUR_TELEGRAM_API:
        return generator(text)
    else:
        return 'Üzgünüm, efendim dışında kimseye hizmet etme yetkim yok.'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'user id: {update.message.chat.id} in {message_type}: {text}')

    if BOT_USERNAME.lower() in text.lower():
        new_text = text.replace(BOT_USERNAME, '')
        response_text = await update.message.reply_text("Processing your request, please wait...")
        response = await handle_response(new_text, update=update)
    else:
        response_text = await update.message.reply_text("Processing your request, please wait...")
        response = await handle_response(text, update=update)

    print(f'bot: {response}')
    await response_text.edit_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == "__main__":
    print('bot started')

    app = Application.builder().token(TOKEN).build()

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Errors 
    app.add_error_handler(error)

    # Polls the bot
    print("polling....")
    app.run_polling(poll_interval=3)