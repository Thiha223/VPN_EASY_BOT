import os
import re
import requests
import telebot

# 1. Fetch Token from GitHub Secrets safely
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Public GitHub repository link that updates free V2Ray/VMess links daily
FREE_VPN_URL = "https://githubusercontent.com"

def fetch_free_configs():
    """Fetches free vmess configurations from public GitHub source"""
    try:
        response = requests.get(FREE_VPN_URL, timeout=10)
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
    
    # Get configuration links from GitHub
    configs = fetch_free_configs()
    
    if configs and len(configs) > 0:
        # Take the first available stable config link from the list
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
    print("VPN Server Bot is officially launched on GitHub Actions...")
    # Start long-polling mechanism
    bot.infinity_polling()
