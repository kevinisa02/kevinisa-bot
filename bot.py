import os
import telebot
import anthropic

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

conversation_history = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Halo! Saya Claude AI. Silakan tanya apa saja!")

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
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=conversation_history[chat_id]
    )
    reply_text = response.content[0].text
    conversation_history[chat_id].append({"role": "assistant", "content": reply_text})
    bot.reply_to(message, reply_text)

bot.polling()
