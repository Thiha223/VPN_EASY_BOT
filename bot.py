import os
import telebot
from flask import Flask, request

# 1. Initialize Bot
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# 2. Initialize Flask Web Server for Render Free Tier
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!", 200

# Webhook Endpoint for Telegram
@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

# Bot commands
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Welcome! This bot is hosted on Render Web Service Free Tier.")

# 3. Main runner
if __name__ == "__main__":
    # Server configuration required by Render
    PORT = int(os.environ.get('PORT', 5000))
    
    # Remove old webhooks and start polling for test
    bot.remove_webhook()
    print(f"Starting server on port {PORT}...")
    
    # Running Flask App
    app.run(host="0.0.0.0", port=PORT)
