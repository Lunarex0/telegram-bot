from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio

TOKEN = "8212749296:AAGivkyfl-Lsh9fsG28UkBcH0bH1H6HkI-Q"
CHAT_ID = -1003339736809  # grubunun ID'si (eksi işaretiyle birlikte!)

async def delete_messages(context: ContextTypes.DEFAULT_TYPE):
    chat_id = CHAT_ID
    messages = await context.bot.get_chat(chat_id)
    # Telegram API tek tek silmeye izin verir, toplu değil.
    async for message in context.bot.get_chat_history(chat_id, limit=100):
        try:
            await context.bot.delete_message(chat_id, message.message_id)
        except:
            pass

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif! Belirli saatlerde mesajları sileceğim.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

scheduler = BackgroundScheduler()

# Her gün sabah 03:00'te çalışsın örneğin:
scheduler.add_job(lambda: asyncio.run(delete_messages(app.bot)), 'cron', hour=3, minute=0)

scheduler.start()
app.run_polling()