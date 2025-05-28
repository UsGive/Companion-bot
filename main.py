import os
from dotenv import load_dotenv
load_dotenv()

import logging
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "I would tell you a joke about construction, but I'm still working on it.",
    "Why did the tomato turn red? Because it saw the salad dressing!"
]

motivations = [
    "Believe in yourself! You can achieve anything.",
    "Every journey begins with a single step.",
    "Stay positive, work hard, and make it happen."
]

productivity_tips = [
    "Focus on one task at a time for better efficiency.",
    "Take regular breaks to maintain your energy levels.",
    "Plan your day ahead to manage your time effectively."
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Tell me a joke", "Motivate me", "Give me a productivity tip"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    if user_message == "Tell me a joke":
        response = random.choice(jokes)
    elif user_message == "Motivate me":
        response = random.choice(motivations)
    elif user_message == "Give me a productivity tip":
        response = random.choice(productivity_tips)
    else:
        response = "Sorry, I didn't understand that. Please select one of the options."

    await update.message.reply_text(response)

async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
