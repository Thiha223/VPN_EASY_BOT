import os
import re
import requests
import telebot

# 1. Fetch Token from GitHub Secrets safely
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# NEW WORKING SOURCE LINK (Updated daily with thousands of active vmess configs)
FREE_VPN_URL = "https://githubusercontent.com"

def fetch_free_configs():
    """Fetches free vmess configurations from active public GitHub source"""
    try:
        response = requests.get(FREE_VPN_URL, timeout=15) # Increased timeout for large list
        if response.status_code == 200:
            # Extract all vmess:// configurations using Regular Expression
            vmess_links = re.findall(r'(vmess://[^\s]+)', response.text)
            return vmess_links
    except Exception as e:
        print(f"Error fetching configs: {e}")
    return []

# Command: /start
@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = (
        "Welcome to VPN PRO Bot! 🇲🇲\n\n"
        "Press /buy to get your high-speed Free VMess VPN configuration link instantly!"
    )
    bot.reply_to(message, welcome_text)

# Command: /buy
@bot.message_handler(commands=['buy'])
def send_vpn(message):
    bot.reply_to(message, "⚡ Fetching the best available server for you... Please wait.")
    
    # Get configuration links from the new GitHub source
    configs = fetch_free_configs()
    
    if configs and len(configs) > 0:
        # Take the first fresh config from the extracted list
        premium_config = configs[0]
        
        success_text = (
            "✅ Server Generated Successfully!\n\n"
            "Here is your Free VMess Config Link:\n"
            f"`{premium_config}`\n\n"
            "📌 *How to use:* Copy the link above and import it into v2rayNG or UTLoop application."
        )
        bot.reply_to(message, success_text, parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ Sorry, servers are temporarily down. Please try again later.")

if __name__ == "__main__":
    print("VPN Server Bot is successfully running with the new source link...")
    bot.infinity_polling()
