import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define the reply keyboard layout
reply_keyboard = [
    ["Ask for Advice", "Explain Like I’m 5"],
    ["Daily Reflection", "Gratitude Prompt"],
    ["Personal Productivity Coach", "Brainstorm Buddy"]
]
keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message with the custom keyboard."""
    welcome_text = "Welcome! Choose one of the options below to get started."
    await update.message.reply_text(welcome_text, reply_markup=keyboard_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond to button presses with a placeholder message."""
    await update.message.reply_text("This feature is coming soon...")

async def get_openai_response(prompt: str) -> str:
    """Generate a response from OpenAI's GPT-4 model."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content'].strip()
    except Exception as error:
        logger.error(f"OpenAI API error: {error}")
        return "Sorry, something went wrong while contacting OpenAI."

async def main() -> None:
    """Launch the Telegram bot."""
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
