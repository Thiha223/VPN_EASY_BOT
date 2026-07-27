import os
import random
import re
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 1. Configuration Settings
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# FIXED ADMIN ID
ADMIN_CHAT_ID = "1678258947"

# 3 Mega Plain Text Sources (Updated daily, 100% stable in Myanmar)
VPN_SOURCES = [
    "https://githubusercontent.com",
    "https://githubusercontent.com",
    "https://githubusercontent.com"
]

def fetch_active_vpn():
    """Fetches and merges configs from multiple active plain text sources to guarantee links"""
    all_links = []
    
    # Try fetching from the sources sequentially
    for url in VPN_SOURCES:
        try:
            response = requests.get(url, timeout=10, verify=False)
            if response.status_code == 200 and response.text:
                # Find all plain vmess:// link strings directly
                found_links = re.findall(r'(vmess://[^\s<>"]+)', response.text)
                if found_links:
                    all_links.extend(found_links)
        except Exception as e:
            print(f"Source error: {e}")
            continue
            
    # If links are found, return one unique random server config
    if all_links and len(all_links) > 0:
        return random.choice(all_links).strip()
        
    return None

# Command: /start
@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = (
        "🚀 Welcome to Premium High-Speed VPN Shop! 🇲🇲\n\n"
        "⚡ Super Fast VMess Server for v2rayNG / UTLoop App.\n"
        "💰 Price: 500 MMK per Premium Server.\n"
        "📌 KBZPay / Wave: `09123456789` (Thiha Aung)\n\n"
        "👉 Please send the **Payment Screenshot (ငွေလွှဲဓာတ်ပုံ)** directly to this bot to unlock your VPN Server instantly!"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

# Handler to capture Payment Photos sent by users
@bot.message_handler(content_types=['photo'])
def handle_payment_photo(message):
    user_id = message.chat.id
    username = message.from_user.username or message.from_user.first_name
    
    bot.reply_to(message, "⏳ သင့်ငွေလွှဲဖြတ်ပိုင်းကို Admin ထံ တင်ပြထားပါသည်။ ခွင့်ပြုချက်ရလျှင် VPN Config ကျလာပါလိမ့်မည်။")
    
    # Create Inline Buttons for Admin Approval
    markup = InlineKeyboardMarkup()
    approve_btn = InlineKeyboardButton("✅ Approve (Send VPN Link)", callback_data=f"approve_vpn_{user_id}")
    reject_btn = InlineKeyboardButton("❌ Reject", callback_data=f"reject_vpn_{user_id}")
    markup.add(approve_btn, reject_btn)
    
    # Forward the photo to Admin with User details
    bot.send_photo(
        ADMIN_CHAT_ID,
        message.photo[-1].file_id,
        caption=f"🔔 **VPN Purchase Request!**\n\n👤 User: {username}\n🆔 ID: `{user_id}`\n\nVerify and choose action:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# Handler for Admin Button Clicks (Approve / Reject)
@bot.callback_query_handler(func=lambda call: True)
def admin_decision(call):
    if call.data.startswith("approve_vpn_"):
        target_user_id = call.data.split("_")[-1]
        
        # Notify Admin that system is fetching link
        bot.answer_callback_query(call.id, "🔄 Fetching server config... please hold.")
        
        # Fetch the active vmess server link directly
        vpn_config = fetch_active_vpn()
        
        if vpn_config:
            success_text = (
                "✅ **Payment Approved by Admin!**\n\n"
                "Here is your Premium High-Speed VMess VPN Configuration Link:\n\n"
                f"`{vpn_config}`\n\n"
                "📌 **How to use:**\n"
                "1. Copy the `vmess://` link text above.\n"
                "2. Open **v2rayNG** or **UTLoop** app.\n"
                "3. Import from clipboard and press Connect!"
            )
            bot.send_message(target_user_id, success_text, parse_mode="Markdown")
            status_text = "\n\n🟢 Status: **APPROVED & VPN CONFIG SENT**"
        else:
            bot.send_message(target_user_id, "❌ Sorry, server pool is empty. Please contact admin for manual key.")
            status_text = "\n\n🟡 Status: **APPROVED BUT SERVER POOL EMPTY**"
            
        # Update Admin Panel Message
        bot.edit_message_caption(
            caption=call.message.caption + status_text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None,
            parse_mode="Markdown"
        )
        
    elif call.data.startswith("reject_vpn_"):
        target_user_id = call.data.split("_")[-1]
        
        # Notify user
        bot.send_message(target_user_id, "❌ **သင့်ငွေလွှဲဖြတ်ပိုင်း မမှန်ကန်သဖြင့် ငြင်းပယ်ခံရပါသည်။** ကျေးဇူးပြု၍ ပြန်လည်စစ်ဆေးပါ။")
        
        # Update Admin Panel Message
        bot.edit_message_caption(
            caption=call.message.caption + "\n\n🔴 Status: **REJECTED**",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None,
            parse_mode="Markdown"
        )

if __name__ == "__main__":
    print("Myanmar Multi-Source VPN Sales Bot is successfully running on GitHub Actions...")
    bot.infinity_polling()
