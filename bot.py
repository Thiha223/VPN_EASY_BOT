import base64
import os
import re
import requests
import telebot
import urllib.parse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 1. Fetch Token safely from GitHub Secrets
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Ultra-stable Base64 & URL Encoded Free VPN Link (Abc Configs Repo)
FREE_VPN_URL = "https://githubusercontent.com"

def fetch_free_configs():
    """Fetches configs, handles Base64, URL decoding, and extracts valid vmess links"""
    try:
        response = requests.get(FREE_VPN_URL, timeout=15, verify=False)
        if response.status_code == 200:
            raw_text = response.text.strip()
            
            # 1. First step: Handle Base64 Padding and Decode
            missing_padding = len(raw_text) % 4
            if missing_padding:
                raw_text += '=' * (4 - missing_padding)
                
            decoded_bytes = base64.b64decode(raw_text)
            decoded_text = decoded_bytes.decode('utf-8', errors='ignore')
            
            # 2. Second step: URL Decode to fix encoded characters
            final_text = urllib.parse.unquote(decoded_text)
            
            # 3. Third step: Extract all clean vmess:// configurations
            vmess_links = re.findall(r'(vmess://[^\s]+)', final_text)
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
        # CRITICAL FIX: Extract ONLY the first single link string from the list array
        single_premium_config = configs[0]
        
        success_text = (
            "✅ Server Generated Successfully!\n\n"
            "Here is your Free VMess Config Link:\n"
            f"`{single_premium_config}`\n\n"
            "📌 *How to use:* Copy the link above and import it into v2rayNG or UTLoop application."
        )
        bot.reply_to(message, success_text, parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ Sorry, servers are temporarily down. Please try again later.")

if __name__ == "__main__":
    print("VPN Server Bot is officially launched with array format fix...")
    bot.infinity_polling()
