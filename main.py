import logging
import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai

load_dotenv()

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

async def get_openai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error fetching response from OpenAI: {e}")
        return "Sorry, I couldn't process that right now."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Tell me a joke", "Motivate me", "Give me a productivity tip"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    prompt = ""

    if user_message == "Tell me a joke":
        prompt = "Tell me a clean short one-line joke."
    elif user_message == "Motivate me":
        prompt = "Give me a short motivational quote."
    elif user_message == "Give me a productivity tip":
        prompt = "Give me a short productivity tip."

    if prompt:
        response = await get_openai_response(prompt)
        await update.message.reply_text(response)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
