# main.py

import os
from dotenv import load_dotenv
load_dotenv()

import logging
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Load bot token from .env file
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Message lists
jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "I told my computer I needed a break, and now it won’t stop sending me Kit-Kats.",
    "I asked the librarian if the library had books on paranoia… she whispered, 'They're right behind you.'",
    "Why did the bicycle fall over? It was two-tired.",
    "I used to play piano by ear, but now I use my hands.",
    "Parallel lines have so much in common… it’s a shame they’ll never meet.",
    "Why was the math book sad? It had too many problems.",
    "I would tell you a construction joke, but I’m still working on it.",
    "I’m reading a book on anti-gravity — it’s impossible to put down!",
    "Why can’t your nose be 12 inches long? Because then it would be a foot.",
    "Did you hear about the claustrophobic astronaut? He just needed a little space.",
    "Why don’t some couples go to the gym? Because some relationships don’t work out.",
    "I used to be indecisive, but now I’m not so sure.",
    "Why do cows wear bells? Because their horns don’t work.",
    "What do you call fake spaghetti? An impasta!",
    "I once got fired from a canned juice company… apparently I couldn’t concentrate.",
    "I ate a clock yesterday. It was very time-consuming.",
    "Why did the scarecrow win an award? Because he was outstanding in his field.",
    "What do you call cheese that isn't yours? Nacho cheese.",
    "What do you call a fish wearing a bowtie? Sofishticated.",
    "I only know 25 letters of the alphabet — I don’t know y.",
    "Why don’t eggs tell jokes? They’d crack each other up.",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "What’s orange and sounds like a parrot? A carrot.",
    "I’m on a seafood diet. I see food and I eat it.",
    "Why did the golfer bring two pairs of pants? In case he got a hole in one.",
    "What’s a skeleton’s least favorite room? The living room.",
    "Did you hear about the guy who invented Lifesavers? He made a mint.",
    "How do you organize a space party? You planet.",
    "Why don’t oysters donate to charity? Because they’re shellfish.",
    "What do you call a pile of cats? A meowtain.",
    "Why did the cookie go to the hospital? Because it felt crummy.",
    "How does a penguin build its house? Igloos it together.",
    "Why did the tomato turn red? Because it saw the salad dressing.",
    "I told my dog 10 jokes. He didn’t laugh once. He’s a husky.",
    "Why did the computer get cold? It left its Windows open.",
    "I used to hate facial hair… but then it grew on me.",
    "What do you get from a pampered cow? Spoiled milk.",
    "Why don’t seagulls fly over the bay? Because then they’d be bagels.",
    "I gave all my dead batteries away—free of charge.",
    "Did you hear the joke about the roof? Never mind, it’s over your head.",
    "I made a pencil with two erasers. It was pointless.",
    "Why can’t you give Elsa a balloon? Because she’ll let it go.",
    "What do you get when you cross a snowman and a dog? Frostbite.",
    "Why are elevator jokes so good? They work on many levels.",
    "My boss told me to have a good day… so I went home.",
    "How do cows stay up to date? They read the moos-paper.",
    "I used to be a baker, but I couldn’t make enough dough.",
    "Why did the gym close down? It just didn’t work out.",
    "How do you make holy water? You boil the hell out of it."
]

motivations = [
    "Believe you can and you're halfway there.",
    "Dream big. Start small. Act now.",
    "You are stronger than you think.",
    "Push yourself, because no one else will.",
    "Don't watch the clock; do what it does. Keep going.",
    "Success is no accident.",
    "Your only limit is you.",
    "Stay positive. Work hard. Make it happen.",
    "Small steps every day.",
    "Doubt kills more dreams than failure ever will.",
    "Progress, not perfection.",
    "Great things never come from comfort zones.",
    "Focus on the goal, not the obstacle.",
    "Discipline is doing it even when you don’t feel like it.",
    "Don’t stop until you’re proud.",
    "Keep going. You’re getting there.",
    "You didn’t come this far to only come this far.",
    "The best time to start was yesterday. The next best is now.",
    "Success begins with self-belief.",
    "Fall seven times, stand up eight.",
    "Work in silence, let success make the noise.",
    "Be so good they can’t ignore you.",
    "The secret of getting ahead is getting started.",
    "Hard work beats talent when talent doesn't work hard.",
    "Act as if it were impossible to fail.",
    "Start where you are. Use what you have. Do what you can.",
    "Focus equals power.",
    "Winners never quit and quitters never win.",
    "Consistency is key.",
    "Strive for progress, not perfection.",
    "If not now, when?",
    "Do something today your future self will thank you for.",
    "Believe in your infinite potential.",
    "One day or day one. You decide.",
    "Make each day your masterpiece.",
    "Stay hungry. Stay foolish.",
    "Success is a series of small wins.",
    "Be fearless in the pursuit of what sets your soul on fire.",
    "Difficult roads lead to beautiful destinations.",
    "Hustle in silence.",
    "Be the energy you want to attract.",
    "You have the power to create change.",
    "It always seems impossible until it’s done.",
    "Don’t limit your challenges. Challenge your limits.",
    "Let your courage be bigger than your fear.",
    "Create the life you can’t wait to wake up to.",
    "Push past your comfort zone.",
    "Success is earned, not given.",
    "You are capable of amazing things.",
    "Keep moving forward."
]

productivity_tips = [
    "Start your day with a to-do list.",
    "Prioritize your most important tasks.",
    "Use the Pomodoro technique: 25 minutes work, 5 minutes break.",
    "Eliminate distractions while working.",
    "Set clear daily goals.",
    "Break big tasks into smaller steps.",
    "Use time blocks for focused work.",
    "Start with the hardest task first (eat the frog).",
    "Limit multitasking — focus on one thing at a time.",
    "Take short breaks to refresh your mind.",
    "Plan your day the night before.",
    "Set deadlines even for open-ended tasks.",
    "Use a planner or digital calendar.",
    "Avoid checking emails constantly.",
    "Declutter your workspace.",
    "Say no to unnecessary meetings.",
    "Turn off notifications during deep work.",
    "Batch similar tasks together.",
    "Use keyboard shortcuts to save time.",
    "Keep your phone out of reach when working.",
    "Automate repetitive tasks when possible.",
    "Review your goals weekly.",
    "Celebrate small wins to stay motivated.",
    "Wake up earlier to gain extra quiet hours.",
    "Reflect on what worked and what didn’t each day.",
    "Limit social media usage during work hours.",
    "Use apps to track your time.",
    "Prepare your work materials in advance.",
    "Drink water and stay hydrated.",
    "Get enough sleep for better focus.",
    "Don’t aim for perfect, aim for done.",
    "Start with 5-minute rule: just begin.",
    "Create a morning routine.",
    "Decline tasks that don’t align with your goals.",
    "Track your progress visually (charts, checklists).",
    "Use noise-canceling headphones for focus.",
    "Finish what you start before starting something new.",
    "Use templates for repetitive tasks.",
    "Stand up and stretch every hour.",
    "Limit decision fatigue by planning meals/outfits.",
    "Avoid overloading your schedule.",
    "Use positive self-talk to stay focused.",
    "Keep your goals visible.",
    "Use two-minute rule: if it takes <2 minutes, do it now.",
    "Set boundaries with people during focus hours.",
    "Review and update your to-do list daily.",
    "Work in a clean, organized environment.",
    "Schedule tasks based on your energy levels.",
    "Keep learning productivity techniques.",
    "Be kind to yourself — progress takes time."
]

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [["Tell me a joke"], ["Motivate me"], ["Give me a productivity tip"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text

    if user_input == "Tell me a joke":
        response = random.choice(jokes)
    elif user_input == "Motivate me":
        response = random.choice(motivations)
    elif user_input == "Give me a productivity tip":
        response = random.choice(productivity_tips)
    else:
        response = "Please use the buttons to choose an option."

    await update.message.reply_text(response)

# Main function to start the bot
def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    logging.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
