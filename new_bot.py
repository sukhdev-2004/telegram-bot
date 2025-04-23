import telebot
import random
import datetime
import pyjokes
import requests
from bs4 import BeautifulSoup
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Your Telegram Bot Token
TOKEN = "7765443029:AAFm-IlGBaXJ6BVYCGbeYSBljEO0xlf7CtA"
bot = telebot.TeleBot(TOKEN)

# Keyboard UI
def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Hello 👋"), KeyboardButton("Tell me a joke 🤣"))
    markup.add(KeyboardButton("How are you?"), KeyboardButton("Help ❓"))
    return markup

# Get Google Snippets and link
def fetch_google_snippets(query):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        search_url = f"https://www.google.com/search?q={query}"
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        snippets = []

        for g in soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd'):
            text = g.get_text()
            if text not in snippets and len(text.split()) > 5:
                snippets.append(text)
            if len(snippets) >= 3:
                break

        if not snippets:
            snippets.append("❗ Sorry, no useful results found.")

        return snippets, f"https://www.google.com/search?q={query.replace(' ', '+')}"
    except Exception as e:
        return [f"❌ Error fetching info: {e}"], None

# Bot /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hi! I’m your smart Google-powered bot. Ask me anything!", reply_markup=get_main_menu())

# Bot /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "💡 Ask me anything! I’ll get info from Google and reply fast.\n\nTry:\n- Who is Elon Musk?\n- Latest Python news\n- IPL 2025 schedule")

# Time & Info
@bot.message_handler(commands=['time'])
def send_time(message):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    bot.send_message(message.chat.id, f"⏰ Current time: {now}")

@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id, "I'm a smart Telegram bot built with Python and Google search.")

# Text handler
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text.strip().lower()

    if "hello" in text or "👋" in text:
        bot.send_message(message.chat.id, "Hello! What would you like to know?")
    elif "how are you" in text:
        bot.send_message(message.chat.id, "Doing great! Ready to help.")
    elif "joke" in text or "🤣" in text:
        bot.send_message(message.chat.id, pyjokes.get_joke())
    elif "quote" in text:
        quotes = [
            "Push yourself, no one else will.",
            "Success is built on consistency.",
            "Be stronger than your excuses."
        ]
        bot.send_message(message.chat.id, random.choice(quotes))
    elif "fact" in text:
        facts = [
            "Sharks existed before trees!",
            "Octopuses have three hearts.",
            "Bananas are berries, but strawberries are not."
        ]
        bot.send_message(message.chat.id, random.choice(facts))
    else:
        bot.send_message(message.chat.id, f"🔍 Searching Google for: `{message.text}`", parse_mode="Markdown")
        snippets, link = fetch_google_snippets(message.text)
        for snippet in snippets:
            bot.send_message(message.chat.id, f"• {snippet}")
        if link:
            bot.send_message(message.chat.id, f"🔗 [Click here for full Google results]({link})", parse_mode="Markdown")

# Stickers & Photos
@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    bot.send_message(message.chat.id, "Cool sticker!")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.send_message(message.chat.id, "Nice photo!")

print("Bot is running...")
bot.polling()
