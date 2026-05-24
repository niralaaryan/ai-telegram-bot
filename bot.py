import os
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
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ==========================================
# TOKENS
# ==========================================

BOT_TOKEN = os.getenv("8924341818:AAHw7lhFd2ubSwYJOZYo03VJT3uHvEvgKvM")
GEMINI_API_KEY = os.getenv("AIzaSyBmF8tJlRhQ34z1_EotShdGNJmF_zoPH8Y")

# ==========================================
# CHECK TOKENS
# ==========================================

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing!")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY missing!")

# ==========================================
# GEMINI SETUP
# ==========================================

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)

# ==========================================
# START COMMAND
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🔥 Advanced AI Telegram Bot Online

Features:
✅ AI Chat
✅ Hindi Support
✅ Coding Help
✅ Study Help
✅ Fast Replies

Send any message.
"""

    await update.message.reply_text(text)

# ==========================================
# HELP COMMAND
# ==========================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    help_text = """
Commands:

/start - Start bot
/help - Help menu
"""

    await update.message.reply_text(help_text)

# ==========================================
# AI CHAT
# ==========================================

async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text

    try:

        response = model.generate_content(user_text)

        reply = response.text

        if len(reply) > 4000:
            reply = reply[:4000]

        await update.message.reply_text(reply)

    except Exception as e:

        await update.message.reply_text(
            f"Error:\n{e}"
        )

# ==========================================
# MAIN
# ==========================================

def main():

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_command)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            ai_chat
        )
    )

    print("BOT RUNNING...")

    app.run_polling()

# ==========================================
# START
# ==========================================

if __name__ == "__main__":
    main()
