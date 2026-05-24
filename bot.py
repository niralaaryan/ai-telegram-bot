import os
import traceback
import logging
import asyncio

print("STARTING BOT...")

try:

    import google.generativeai as genai

    from telegram import Update
    from telegram.ext import (
        Application,
        CommandHandler,
        MessageHandler,
        filters,
        ContextTypes
    )

    print("IMPORTS SUCCESS")

    logging.basicConfig(level=logging.INFO)

    BOT_TOKEN = os.getenv("8924341818:AAHw7lhFd2ubSwYJOZYo03VJT3uHvEvgKvM")
    GEMINI_API_KEY = os.getenv("AIzaSyDcOWamA94-NeJ1uptjSE-KKc3WYX23NrU")

    print("BOT TOKEN EXISTS:", bool(BOT_TOKEN))
    print("GEMINI EXISTS:", bool(GEMINI_API_KEY))

    if not BOT_TOKEN:
        raise Exception("BOT_TOKEN NOT FOUND")

    if not GEMINI_API_KEY:
        raise Exception("GEMINI_API_KEY NOT FOUND")

    genai.configure(
        api_key=GEMINI_API_KEY
    )

    print("GEMINI CONFIGURED")

    model = genai.GenerativeModel(
        "gemini-1.5-flash"
    )

    print("MODEL LOADED")

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

        await update.message.reply_text(
            "🔥 Bot Online!"
        )

    async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

        try:

            user_text = update.message.text

            response = model.generate_content(
                user_text
            )

            await update.message.reply_text(
                response.text[:4000]
            )

        except Exception as e:

            await update.message.reply_text(
                str(e)
            )

    async def main():

        print("BUILDING APP")

        app = Application.builder().token(
            BOT_TOKEN
        ).build()

        print("ADDING HANDLERS")

        app.add_handler(
            CommandHandler("start", start)
        )

        app.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat
            )
        )

        print("INITIALIZING")

        await app.initialize()

        print("STARTING")

        await app.start()

        print("POLLING")

        await app.updater.start_polling()

        print("BOT RUNNING SUCCESSFULLY")

        while True:
            await asyncio.sleep(3600)

    asyncio.run(main())

except Exception as e:

    print("\n===== FULL ERROR =====\n")

    traceback.print_exc()

    print("\n======================\n")
