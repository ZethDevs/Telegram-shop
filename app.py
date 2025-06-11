from flask import Flask, render_template
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import threading
import os

app = Flask(__name__)

API_TOKEN = '8197249734:AAENVrafLfqfP6ztJ7XvooLauJs2I3VYnCg'
ADMIN_CHAT_ID = 5937612986  # Replace with your Telegram user ID
bot = telebot.TeleBot(API_TOKEN)

PAYPAL_EMAIL = "lutfi.faridd@gmail.com"
CRYPTO_WALLET = {
    "Binance Pay (UID)": "834275463",
    "USDT (TRC20)": "TGGctftGUNVXLLHr4GrQBNkfn7LkBRH1ca"
}

products = {
    1: {
        "name": "Bot Decryptor VPN (Telegram)",
        "desc": "Bot can decrypt any VPN configuration.",
        "price": 20,
        "image_url": "https://i.ibb.co/5g9tdxd1/5e1ae97e-5b9a-482b-a048-0d47afc40bf2-screenshot-2024-10-24-11-08-02-137-edit-org-telegram-messenger.jpg",
        "status": "Ready",
    },
    2: {
        "name": "SSC Lua (SSH + Note + DNS)",
        "desc": "Script Lua for decrypt SSH CUSTOM.",
        "price": 10,
        "image_url": "https://i.ibb.co/j90gR7jJ/IMG-20250610-110941.jpg",
        "status": "Ready",
    },
    3: {
        "name": "Mod APK Unlocker (OpenTunnel v1.0.7 Latest)",
        "desc": "Mod Apk Unlocker using inject Log Decrypt Full config.",
        "price": 3,
        "image_url": "https://i.ibb.co/wFWyNRSG/Screenshot-2025-06-10-11-05-35-614-edit-bin-mt-plus-canary.jpg",
        "status": "Ready",
    },
    4: {
        "name": "Mod APK Unlocker (ZIVPN Tunnel v2.0.3 Latest)",
        "desc": "Mod Apk Unlocker using inject Log Decrypt Full config.",
        "price": 3,
        "image_url": "https://i.ibb.co/LbwgSgR/Screenshot-2025-06-11-07-15-25-754-edit-bin-mt-plus-canary.jpg",
        "status": "Ready",
    },
    5: {
        "name": "JSHook (Opentunnel)",
        "desc": "exclusive script for decrypt OpenTunnel Injector.",
        "price": 30,
        "image_url": "https://i.ibb.co/1BZXFTB/IMG-20250610-113011.jpg",
        "status": "Ready",
    },
    6: {
        "name": "JSHook (e-v2ray)",
        "desc": "exclusive script for decrypt e-v2ray Injector.",
        "price": 30,
        "image_url": "https://i.ibb.co/GfwZqkMd/IMG-20250610-113033.jpg",
        "status": "Ready",
    },
    7: {
        "name": "JSHook (ZIVPN Tunnel)",
        "desc": "exclusive script for decrypt ZIVPN Tunnel Injector.",
        "price": 30,
        "image_url": "https://i.ibb.co/hFbc0r8v/file-00000000f898622faa3931383e04bb3f.png",
        "status": "Coming soon",
    },
}

pending_payment = {}
admin_order_refs = {}

@app.route('/')
def index():
    return render_template('index.html', products=products)

@bot.message_handler(commands=['start'])
def show_products(message):
    send_product_list(message.chat.id)

def send_product_list(chat_id):
    markup = InlineKeyboardMarkup()
    for pid, p in products.items():
        markup.add(InlineKeyboardButton(p['name'], callback_data=f"view_{pid}"))
    bot.send_message(chat_id, "👋 *Welcome to Nathan - STORE*\n\nThis is your time for be best decryptor. 😈\nYou’ll enjoy use tools from us — stay alert!\n\n_We provide high-quality scripts and tools for decrypting VPN configuration._\n\n*/free to get free script from us.*\n```\n━━━━━━━━━━━━━━━━━\n👑 Products Available : 7\n💵 >Total Transaction : 17\n```", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(commands=['cancel'])
def cancel(message):
    chat_id = message.chat.id
    if chat_id in pending_payment:
        pending_payment.pop(chat_id)
        bot.send_message(chat_id, "\u274C Your order has been canceled.")
    else:
        bot.send_message(chat_id, "You don't have any active order.")

@bot.message_handler(commands=["free"])
def handle_free(message):
    bot.reply_to(
        message,
        "There is a special gift from someone for you :\n"
        "===========❤️🐣❤️===========\n"
        "Thanks to @Leneath"
    )
    gift_path = os.path.join(os.getcwd(), "LinkLayerVPN.lua")
    if os.path.exists(gift_path):
        with open(gift_path, "rb") as gift:
            bot.send_document(message.chat.id, gift, caption="────────────────\n• Target : LinkLayer VPN\n• Extension : .Ink\nType : Auto Print Lua ✅")
    else:
        bot.send_message(message.chat.id, "\u274C Gift file not found.")

@bot.callback_query_handler(func=lambda call: True)
def handle_buttons(call):
    chat_id = call.message.chat.id

    if call.data.startswith("view_"):
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass

        pid = int(call.data.split("_")[1])
        p = products[pid]
        caption = (
            f"╭─────────────────╮\n│ *Product ID :* `{pid}`\n"
            f"│ *Name :* `{p['name']}`\n"
            f"│ *Description :* \n│ _{p['desc']}_\n├──────────────────\n"
            f"│ \U0001F4B5 *Price :* `${p['price']}`\n"
            f"│ \U0001F4E6 *Status :* `{p['status']}`\n╰─────────────────╯"
        )
        markup = InlineKeyboardMarkup(row_width=2)
        if p['status'].lower() == "ready":
            markup.add(
                InlineKeyboardButton("\U0001F4B3 Buy Now", callback_data=f"buy_{pid}"),
                InlineKeyboardButton("\U0001F519 Back to Products", callback_data="back_to_menu")
            )
        bot.send_photo(chat_id, p['image_url'], caption=caption, parse_mode='Markdown', reply_markup=markup)

    elif call.data == "back_to_menu":
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass
        send_product_list(chat_id)

    elif call.data.startswith("buy_"):
        pid = int(call.data.split("_")[1])
        p = products[pid]
        pending_payment[chat_id] = {
            "pid": pid,
            "product": p
        }

        instruction = (
            f"╭─────────────────╮\n│ \U0001F9FE *Purchase :* `{p['name']}`\n"
            f"│ \U0001F4B0 *Price :* `${p['price']}`\n╰─────────────────╯\n"
            f"\U0001F4CC *Payment Instructions:*\n"
            f"☕ Donate via ko-fi : [Nathanaeru](https://ko-fi.com/nathanaeru#checkoutModal)\n"
            f"💳 Pay via Paypal : [Nathanaeru](https://www.paypal.me/imlutfifarid)\n"
        )
        for name, wallet in CRYPTO_WALLET.items():
            instruction += f"🪙 Pay via {name} : `{wallet}`\n"

        instruction += (
            "\n\U0001F4E4 Please *send a photo* of your payment proof.\n"
            "We will verify your payment and deliver your product.\n\n"
            "Use /cancel to cancel this order."
        )

        sent_msg = bot.send_message(chat_id, instruction, parse_mode='Markdown', disable_web_page_preview=True)
        pending_payment[chat_id]["msg_id"] = sent_msg.message_id

@bot.message_handler(content_types=['photo'])
def handle_payment_proof(message):
    chat_id = message.chat.id
    full_name = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()
    user_aidi = message.from_user.username
    #print(f"Username: {message.from_user.username}")
    if chat_id not in pending_payment:
        bot.send_message(chat_id, "\u2757 You have no active order. Use /menu to start shopping.")
        return

    p = pending_payment[chat_id]["product"]
    ref_id = str(int(time.time() * 1000))

    admin_order_refs[ref_id] = {
        "buyer_id": message.from_user.id,
        "username": message.from_user.username or message.from_user.first_name,
        "chat_id": chat_id,
        "instruction_msg_id": pending_payment[chat_id].get("msg_id")
    }

    caption = (
        f"\U0001F4E5 *Payment Proof Received*\n"
        f"\U0001F6D2 Product: {p['name']}\n"
        f"\U0001F4B5 Price: ${p['price']}\n"
        f"👤 Buyer: {full_name}\n"
        f"👤 usernane : @{user_aidi}\n"
        f"\U0001F194 Ref ID: {ref_id}"
    )

    bot.send_photo(ADMIN_CHAT_ID, message.photo[-1].file_id, caption=caption, parse_mode='Markdown')
    bot.send_message(chat_id, "\u2705 Your payment proof has been submitted. Please wait for confirmation.")
    pending_payment.pop(chat_id)

@bot.message_handler(content_types=['document', 'text'], func=lambda msg: msg.reply_to_message and msg.chat.id == ADMIN_CHAT_ID)
def handle_admin_reply(msg):
    reply = msg.reply_to_message
    if not reply.caption or "Ref ID:" not in reply.caption:
        bot.send_message(ADMIN_CHAT_ID, "\u26A0\ufe0f Please reply to a valid payment proof message containing a Ref ID.")
        return

    try:
        ref_id_line = [line for line in reply.caption.splitlines() if "Ref ID:" in line][0]
        ref_id = ref_id_line.split(":")[-1].strip()
        order = admin_order_refs.get(ref_id)

        if not order:
            bot.send_message(ADMIN_CHAT_ID, "\u274C Reference ID not found.")
            return

        buyer_id = order["buyer_id"]
        chat_id = order["chat_id"]
        instruction_msg_id = order.get("instruction_msg_id")

        if msg.content_type == "document":
            bot.send_document(buyer_id, msg.document.file_id, caption="\U0001F4E6 Here is your order. Thank you!")
        else:
            bot.send_message(buyer_id, f"Nathan Payment API System :\n{msg.text}\n──────────────────")

        if instruction_msg_id:
            try:
                bot.delete_message(chat_id, instruction_msg_id)
            except:
                pass

        bot.send_message(ADMIN_CHAT_ID, f"\u2705 Sent to buyer ID `{buyer_id}`", parse_mode='Markdown')
        del admin_order_refs[ref_id]

    except Exception as e:
        bot.send_message(ADMIN_CHAT_ID, f"\u274C Error: {e}")

def start_bot():
    bot.polling(non_stop=True)

if __name__ == '__main__':
    threading.Thread(target=start_bot).start()
    app.run(host='0.0.0.0', port=5000)
