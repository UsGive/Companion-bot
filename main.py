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
        logging.error(f"OpenAI API error: {e}")
        return "Sorry, I encountered an error processing your request."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Tell me a joke", "Motivate me", "Give me a productivity tip"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompts = {
        "Tell me a joke": "Tell me a clean short one-line joke.",
        "Motivate me": "Give me a short motivational quote.",
        "Give me a productivity tip": "Give me a short productivity tip."
    }

    user_message = update.message.text
    prompt = prompts.get(user_message)

    if prompt:
        response = await get_openai_response(prompt)
        await update.message.reply_text(response)

if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()
