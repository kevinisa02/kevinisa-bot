import os
import telebot
from openai import OpenAI

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
API_KEY = os.environ.get("FREEMODEL_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.freemodel.dev/v1"
)

conversation_history = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Halo! Saya AI Assistant. Silakan tanya apa saja!")

@bot.message_handler(commands=['reset'])
def reset(message):
    conversation_history[message.chat.id] = []
    bot.reply_to(message, "Percakapan direset!")

@bot.message_handler(func=lambda m: True)
def reply(message):
    chat_id = message.chat.id
    if chat_id not in conversation_history:
        conversation_history[chat_id] = []
    conversation_history[chat_id].append({"role": "user", "content": message.text})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history[chat_id]
    )
    reply_text = response.choices[0].message.content
    conversation_history[chat_id].append({"role": "assistant", "content": reply_text})
    bot.reply_to(message, reply_text)

bot.polling()
