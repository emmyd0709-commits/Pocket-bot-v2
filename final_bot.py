import os
import time
import random
import threading
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("BOT_TOKEN")

PAIRS = ["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "EUR/GBP OTC", "BTC/USD OTC", "USD/CHF OTC"]
DIRECTIONS = ["CALL ⬆️", "PUT ⬇️"]

def get_one_signal():
    pair = random.choice(PAIRS)
    direction = random.choice(DIRECTIONS)
    expiry = random.choice([1, 2, 4])
    strength = random.randint(78, 97)
    return f"📊 {pair}\n➡️ {direction} | {expiry} min | {strength}%"

def get_buttons():
    keyboard = [
        [InlineKeyboardButton("🔔 New Signal", callback_data='new_signal'),
         InlineKeyboardButton("📊 3-5 Signals", callback_data='many_signals')],
        [InlineKeyboardButton("⏱️ 1 Min Timer", callback_data='timer_1'),
         InlineKeyboardButton("⏱️ 4 Min Timer", callback_data='timer_4')],
        [InlineKeyboardButton("🔄 Refresh", callback_data='refresh')]
    ]
    return InlineKeyboardMarkup(keyboard)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🔥 *POCKET BOT V2 PRO* 🔥\n\nTap button below, no need to type command again 👇",
        parse_mode='Markdown',
        reply_markup=get_buttons()
    )

def signal_cmd(update: Update, context: CallbackContext):
    sig = get_one_signal()
    update.message.reply_text(f"🔔 *SIGNAL*\n\n{sig}", parse_mode='Markdown', reply_markup=get_buttons())

def signals_cmd(update: Update, context: CallbackContext):
    count = random.randint(3, 5)
    text = f"🔔 *{count} SIGNALS*\n\n"
    for i in range(1, count+1):
        text += f"{i}. {get_one_signal()}\n\n"
    update.message.reply_text(text, parse_mode='Markdown', reply_markup=get_buttons())

def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    if data == 'new_signal':
        sig = get_one_signal()
        query.edit_message_text(
            f"🔔 *NEW SIGNAL*\n\n{sig}\n\nTap for another 👇",
            parse_mode='Markdown',
            reply_markup=get_buttons()
        )
    elif data == 'many_signals':
        count = random.randint(3, 5)
        text = f"🔔 *{count} SIGNALS*\n\n"
        for i in range(1, count+1):
            text += f"{i}. {get_one_signal()}\n\n"
        query.edit_message_text(text, parse_mode='Markdown', reply_markup=get_buttons())
    elif data.startswith('timer_'):
        minutes = int(data.split('_')[1])
        msg = query.edit_message_text(
            f"📊 *TRADE STARTED*\n⏱️ {minutes:02d}:00",
            parse_mode='Markdown',
            reply_markup=get_buttons()
        )
        thread = threading.Thread(target=countdown_thread, args=(msg, minutes))
        thread.daemon = True
        thread.start()
    elif data == 'refresh':
        query.edit_message_text("🔄 Ready! Tap button 👇", parse_mode='Markdown', reply_markup=get_buttons())

def countdown_thread(msg, minutes):
    total_seconds = minutes * 60
    for sec in range(total_seconds, -1, -1):
        m = sec // 60
        s = sec % 60
        if sec == 0:
            try: msg.edit_text("✅ *TRADE CLOSED* - Tap new signal 👇", parse_mode='Markdown', reply_markup=get_buttons())
            except: pass
            break
        if sec % 5 == 0:
            try: msg.edit_text(f"📊 *TRADE RUNNING*\n⏱️ {m:02d}:{s:02d}", parse_mode='Markdown', reply_markup=get_buttons())
            except: pass
        time.sleep(1)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("signal", signal_cmd, run_async=True))
    dp.add_handler(CommandHandler("signals", signals_cmd, run_async=True))
    dp.add_handler(CallbackQueryHandler(button_click))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
