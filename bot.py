import os
import telebot

# Fetch the token from Render Environment Variables safely
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Handler for /start command
@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = "Welcome to Free VPN Bot! Use /buy to get a free configuration link."
    bot.reply_to(message, welcome_text)

# Keep the bot running continuously
if __name__ == "__main__":
    print("Bot is successfully running...")
    bot.infinity_polling()
