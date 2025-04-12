from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import datetime

BOT_TOKEN = "8097774842:AAHdvTaYGkERO-qdizZ45HKUQINNtNlW_EQ"

def format_info(user, chat, message):
    now = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    return f"""🕵️‍♂️ *Thông tin Telegram của bạn:*

👤 *Họ tên:* `{user.first_name}`
🔤 *Username:* `@{user.username}`""" + ("" if user.username else "`Không có`") + f"""
🆔 *Chat ID:* `{chat.id}`
🌐 *Ngôn ngữ:* `{user.language_code}`
💬 *Lệnh dùng:* `{message.text}`
👥 *Loại chat:* `{chat.type}`
📅 *Thời gian:* `{now}`
"""

def handle_thongtin(update: Update, context: CallbackContext):
    user = update.message.from_user
    chat = update.message.chat
    info = format_info(user, chat, update.message)

    keyboard = [[InlineKeyboardButton("📋 Sao chép", callback_data='copy_info')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=chat.id, text=info, reply_markup=reply_markup, parse_mode='Markdown')

def copy_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    chat = query.message.chat

    copied_text = format_info(user, chat, query.message)
    context.bot.send_message(chat_id=chat.id, text="📄 *Đã sao chép nội dung:*", parse_mode='Markdown')
    context.bot.send_message(chat_id=chat.id, text=f"`{copied_text}`", parse_mode='Markdown')
    query.answer("Đã gửi nội dung để sao chép!")

updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# ✅ Chỉ lắng nghe lệnh /thongtin
dispatcher.add_handler(CommandHandler("thongtin", handle_thongtin))
dispatcher.add_handler(CallbackQueryHandler(copy_button, pattern='copy_info'))

print("✅ Bot đang chạy - Gõ /thongtin để nhận thông tin")
updater.start_polling()
updater.idle()
