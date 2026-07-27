import base64
import os
import re
import requests
import telebot
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 1. Fetch Token safely from GitHub Secrets
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Ultra-stable Base64 Encoded Free VPN Subscription Link
FREE_VPN_URL = "https://githubusercontent.com"

def fetch_free_configs():
    """Fetches base64 encoded configs, decodes them, and extracts vmess:// links"""
    try:
        response = requests.get(FREE_VPN_URL, timeout=15, verify=False)
        if response.status_code == 200:
            raw_text = response.text.strip()
            
            # Base64 Decoding Process with padding correction
            missing_padding = len(raw_text) % 4
            if missing_padding:
                raw_text += '=' * (4 - missing_padding)
                
            decoded_bytes = base64.b64decode(raw_text)
            decoded_text = decoded_bytes.decode('utf-8', errors='ignore')
            
            # Extract all decoded vmess:// configurations using Regular Expression
            vmess_links = re.findall(r'(vmess://[^\s]+)', decoded_text)
            return vmess_links
    except Exception as e:
        print(f"Error fetching/decoding configs: {e}")
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
    
    # Get decrypted configuration links from the source
    configs = fetch_free_configs()
    
    if configs and len(configs) > 0:
        # Pick the very first active decrypted vmess:// link from the list
        premium_config = configs
        
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
    print("VPN Server Bot is successfully running with Base64 Decoder...")
    bot.infinity_polling()
