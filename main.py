import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up OpenAI API
openai.api_key = OPENAI_API_KEY

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Define the reply keyboard
keyboard = [
    ["Ask for Advice", "Explain Like I’m 5"],
    ["Daily Reflection", "Gratitude Prompt"],
    ["Personal Productivity Coach", "Brainstorm Buddy"]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Welcome message handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! I’m your AI-powered assistant. Choose a button to get started:",
        reply_markup=reply_markup
    )

# Placeholder message
COMING_SOON_MESSAGE = "This feature is coming soon..."

# Main message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    if user_message == "Ask for Advice":
        await update.message.reply_text(COMING_SOON_MESSAGE)
        # === INSERT FEATURE LOGIC HERE LATER ===
        # response = await get_openai_response("Your prompt here")
        # await update.message.reply_text(response)

    elif user_message == "Explain Like I’m 5":
        await update.message.reply_text(COMING_SOON_MESSAGE)
        # === INSERT FEATURE LOGIC HERE LATER ===

    elif user_message == "Daily Reflection":
        await update.message.reply_text(COMING_SOON_MESSAGE)
        # === INSERT FEATURE LOGIC HERE LATER ===

    elif user_message == "Gratitude Prompt":
        await update.message.reply_text(COMING_SOON_MESSAGE)
        # === INSERT FEATURE LOGIC HERE LATER ===

    elif user_message == "Personal Productivity Coach":
        await update.message.reply_text(COMING_SOON_MESSAGE)
        # === INSERT FEATURE LOGIC HERE LATER ===

    elif user_message == "Brainstorm Buddy":
        await update.message.reply_text(COMING_SOON_MESSAGE)
        # === INSERT FEATURE LOGIC HERE LATER ===

    else:
        await update.message.reply_text("Please choose one of the buttons.")

# Function to get response from OpenAI
async def get_openai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        return "Sorry, something went wrong with the AI response."

# Main function to run the bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
