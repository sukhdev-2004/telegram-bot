import telebot
import random
import datetime
import pyjokes
import wikipedia
from googlesearch import search
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Telegram Bot Token
TOKEN = "7765443029:AAFm-IlGBaXJ6BVYCGbeYSBljEO0xlf7CtA"
bot = telebot.TeleBot(TOKEN)

# Set Wikipedia language
wikipedia.set_lang("en")

# Keyboard Buttons
def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Hello 👋"), KeyboardButton("Tell me a joke 🤣"))
    markup.add(KeyboardButton("How are you?"), KeyboardButton("Help ❓"))
    return markup

# /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello! I'm your smart Telegram bot. Choose an option below.", reply_markup=get_main_menu())

# /help command
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """Here are some things I can do:
• Tell jokes
• Share fun facts
• Show a random quote
• Answer general questions using Wikipedia and Google
Just type your request or use the buttons below."""
    bot.send_message(message.chat.id, help_text)

# /info and /time
@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id, "I'm a Telegram bot built with Python and Telebot!")

@bot.message_handler(commands=['time'])
def send_time(message):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    bot.send_message(message.chat.id, f"⏰ Current time: {now}")

# Wikipedia command with Google fallback
@bot.message_handler(commands=['wiki'])
def wiki_search(message):
    query = message.text.replace("/wiki", "").strip()
    if not query:
        bot.send_message(message.chat.id, "❗ Type something after /wiki like `/wiki moon`", parse_mode='Markdown')
        return
    try:
        summary = wikipedia.summary(query, sentences=3)
        bot.send_message(message.chat.id, f"📚 QuickBot says:\n\n{summary}")
    except:
        bot.send_message(message.chat.id, "❌ Couldn't fetch from Wikipedia. Trying Google...")

    # Always return Google results for more info
    try:
        bot.send_message(message.chat.id, "🔍 Top Google results:")
        for result in search(query, num_results=5):
            bot.send_message(message.chat.id, result)
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Google search failed: {e}")

# General Text Message Handler
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text.lower()

    if "hello" in text or "👋" in text:
        bot.send_message(message.chat.id, "Hi there! How can I assist you?")
    elif "how are you" in text:
        bot.send_message(message.chat.id, "I'm doing great, thanks! 🤖")
    elif "joke" in text or "🤣" in text:
        bot.send_message(message.chat.id, pyjokes.get_joke())
    elif "quote" in text or "🌟" in text:
        quotes = [
            "Believe in yourself and all that you are.",
            "Push yourself, because no one else is going to do it for you.",
            "Great things never come from comfort zones.",
            "Don’t wait for opportunity. Create it."
        ]
        bot.send_message(message.chat.id, random.choice(quotes))
    elif "fact" in text or "🎭" in text:
        facts = [
            "Octopuses have three hearts.",
            "Honey never spoils.",
            "Sharks existed before trees!",
            "Bananas are berries, but strawberries aren’t."
        ]
        bot.send_message(message.chat.id, random.choice(facts))
    elif "help" in text:
        send_help(message)
    elif text.startswith("who is") or text.startswith("what is") or text.startswith("search"):
        query = text.replace("who is", "").replace("what is", "").replace("search", "").strip()
        if not query:
            bot.send_message(message.chat.id, "❗ Type something like `who is Elon Musk`.")
            return
        try:
            summary = wikipedia.summary(query, sentences=3)
            bot.send_message(message.chat.id, f"📚 QuickBot says:\n\n{summary}")
        except:
            bot.send_message(message.chat.id, "❌ Couldn't fetch from Wikipedia.")

        # Google search fallback
        try:
            bot.send_message(message.chat.id, "🔍 Here are 5 top results:")
            for result in search(query, num_results=5):
                bot.send_message(message.chat.id, result)
        except Exception as e:
            bot.send_message(message.chat.id, f"⚠️ search failed: {e}")
    else:
        bot.send_message(message.chat.id, "I'm not sure what you mean!")

# Handle stickers
@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    bot.send_message(message.chat.id, "Nice sticker! 😎")

# Handle photos
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.send_message(message.chat.id, "Cool photo! 📸")

print("Bot is running...")
bot.polling()
