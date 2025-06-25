from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

BOT_TOKEN = "ТВОЙ_ТОКЕН_ОТ_BOTFATHER"  # ← Замени на свой токен

# 👋 Приветствие
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"Привет, {user}! 👋\n"
        "Я умею скачивать видео из:\n"
        "📌 TikTok\n📌 Instagram\n\n"
        "Просто пришли мне ссылку, и я скачаю видео для тебя 📥"
    )

# 📥 Обработка входящих ссылок
async def handle_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "tiktok.com" in url:
        await download_tiktok(update, url)
    elif "instagram.com" in url:
        await download_instagram(update, url)
    else:
        await update.message.reply_text("😕 Я поддерживаю только ссылки из TikTok и Instagram.")

# 📹 TikTok загрузка
async def download_tiktok(update, url):
    await update.message.reply_text("📲 Скачиваю видео из TikTok...")
    try:
        api_url = f"https://tikwm.com/api/?url={url}"
        response = requests.get(api_url)
        data = response.json()
        video_url = data["data"]["play"]
        await update.message.reply_video(video=video_url)
    except:
        await update.message.reply_text("❌ Не удалось скачать TikTok-видео.")

# 📷 Instagram загрузка
async def download_instagram(update, url):
    await update.message.reply_text("📲 Скачиваю видео из Instagram...")
    try:
        api = "https://saveig.app/api/ajaxSearch"
        headers = {
            "x-requested-with": "XMLHttpRequest",
            "referer": "https://saveig.app/"
        }
        payload = {"q": url}
        response = requests.post(api, data=payload, headers=headers)
        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            video_url = data["data"][0]["url"]
            await update.message.reply_video(video=video_url)
        else:
            await update.message.reply_text("⚠️ Видео не найдено или оно приватное.")
    except:
        await update.message.reply_text("❌ Ошибка при скачивании Instagram-видео.")

# 🚀 Запуск бота
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_links))
app.run_polling()