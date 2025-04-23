import telebot
import random
import datetime
import pyjokes
import requests
from bs4 import BeautifulSoup
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Telegram Bot Token
TOKEN = "7765443029:AAFm-IlGBaXJ6BVYCGbeYSBljEO0xlf7CtA"
bot = telebot.TeleBot(TOKEN)

# Keyboard Buttons
def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Hello 👋"), KeyboardButton("Tell me a joke 🤣"))
    markup.add(KeyboardButton("How are you?"), KeyboardButton("Help ❓"))
    return markup

# Fetch Google Snippets
def fetch_google_snippets(query):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        search_url = f"https://www.google.com/search?q={query}"
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        snippets = []

        for g in soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd'):
            text = g.get_text()
            if text not in snippets and len(text.split()) > 5:
                snippets.append(text)
            if len(snippets) >= 5:
                break
        return snippets or ["Sorry, I couldn't find anything useful."]
    except Exception as e:
        return [f"Error fetching from Google: {e}"]

# /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello! I'm your smart Telegram bot. Choose an option below.", reply_markup=get_main_menu())

# /help command
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """Here are some things I can do:
• Tell jokes
• Share fun facts or quotes
• Answer general questions using Google
Just type anything you want to know or use the buttons."""
    bot.send_message(message.chat.id, help_text)

# /info and /time
@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id, "I'm a Telegram bot powered by Google search and Python!")

@bot.message_handler(commands=['time'])
def send_time(message):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    bot.send_message(message.chat.id, f"⏰ Current time: {now}")

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
    else:
        bot.send_message(message.chat.id, f"🔍 Searching Google for: {text}")
        snippets = fetch_google_snippets(text)
        for snippet in snippets:
            bot.send_message(message.chat.id, f"• {snippet}")

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
