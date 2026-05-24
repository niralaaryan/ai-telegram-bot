import os
import asyncio
import logging
import google.generativeai as genai

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# ==========================================
# LOGGING
# ==========================================

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# ==========================================
# TOKENS
# ==========================================

BOT_TOKEN = os.getenv("8924341818:AAHw7lhFd2ubSwYJOZYo03VJT3uHvEvgKvM")
GEMINI_API_KEY = os.getenv("AIzaSyDcOWamA94-NeJ1uptjSE-KKc3WYX23NrU")

print("BOT TOKEN FOUND:", bool(BOT_TOKEN))
print("GEMINI FOUND:", bool(GEMINI_API_KEY))

# ==========================================
# CHECK TOKENS
# ==========================================

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN missing")

if not GEMINI_API_KEY:
    raise Exception("GEMINI_API_KEY missing")

# ==========================================
# GEMINI
# ==========================================

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)

# ==========================================
# COMMANDS
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 AI Bot Online!"
    )

# ==========================================
# CHAT
# ==========================================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text

    try:

        response = model.generate_content(
            user_text
        )

        text = response.text[:4000]

        await update.message.reply_text(text)

    except Exception as e:

        logger.error(e)

        await update.message.reply_text(
            f"Error:\n{e}"
        )

# ==========================================
# MAIN
# ==========================================

async def main():

    app = Application.builder().token(
        BOT_TOKEN
    ).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat
        )
    )

    print("BOT RUNNING...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(3600)

# ==========================================
# START
# ==========================================

if __name__ == "__main__":

    asyncio.run(main())
