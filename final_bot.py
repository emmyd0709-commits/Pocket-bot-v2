import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")

def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("📈 Get Signal", callback_data='signal')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome boss! Your private Pocket Bot ready.", reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="✅ Signal: BUY EUR/USD - 1 min | Confidence 85%")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
