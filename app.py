from flask import Flask, render_template
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import threading
import os
import datetime

app = Flask(__name__)

API_TOKEN = '7814162622:AAGHkS152cNIDjwBUAV0rVSoOkeuZVRG5rM'
ADMIN_CHAT_ID = 5937612986
bot = telebot.TeleBot(API_TOKEN)

start_time = time.time()

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
        "category": "Bot"
    },
    2: {
        "name": "SSC Lua (SSH + Note + DNS)",
        "desc": "Script Lua for decrypt SSH CUSTOM.",
        "price": 10,
        "image_url": "https://i.ibb.co/j90gR7jJ/IMG-20250610-110941.jpg",
        "status": "Ready",
        "category": "Lua"
    },
    3: {
        "name": "Mod APK Unlocker (OpenTunnel v1.0.7 Latest)",
        "desc": "Mod Apk Unlocker using inject Log Decrypt Full config.",
        "price": 3,
        "image_url": "https://i.ibb.co/wFWyNRSG/Screenshot-2025-06-10-11-05-35-614-edit-bin-mt-plus-canary.jpg",
        "status": "Ready",
        "category": "Mod"
    },
    4: {
        "name": "Mod APK Unlocker (ZIVPN Tunnel v2.0.3 Latest)",
        "desc": "Mod Apk Unlocker using inject Log Decrypt Full config.",
        "price": 3,
        "image_url": "https://i.ibb.co/LbwgSgR/Screenshot-2025-06-11-07-15-25-754-edit-bin-mt-plus-canary.jpg",
        "status": "Ready",
        "category": "Mod"
    },
    5: {
        "name": "Unlocker & Python (HTTP CUSTOM v5.11.29-RC90 Latest)",
        "desc": "Mod Apk Unlocker using inject Log Decrypt SSH/V2ray/OpenVPN/Psiphon/UDP",
        "price": 25,
        "image_url": "https://i.ibb.co/kszF2DKw/IMG-20250617-175644-721.jpg",
        "status": "Ready",
        "category": "Mod"
    },
    6: {
        "name": "JSHook (Opentunnel)",
        "desc": "exclusive script for decrypt OpenTunnel Injector.",
        "price": 15,
        "image_url": "https://i.ibb.co/1BZXFTB/IMG-20250610-113011.jpg",
        "status": "Ready",
        "category": "JSHook"
    },
    7: {
        "name": "JSHook (e-v2ray)",
        "desc": "exclusive script for decrypt e-v2ray Injector.",
        "price": 15,
        "image_url": "https://i.ibb.co/GfwZqkMd/IMG-20250610-113033.jpg",
        "status": "Ready",
        "category": "JSHook"
    },
    8: {
        "name": "JSHook (SocksHTTP Plus)",
        "desc": "exclusive script for decrypt sksplus.",
        "price": 10,
        "image_url": "https://i.ibb.co/j9hRkFb8/IMG-20250619-050008.jpg",
        "status": "Ready",
        "category": "JSHook"
    },
    9: {
        "name": "JSHook (SocksHTTP)",
        "desc": "exclusive script for decrypt sks.",
        "price": 10,
        "image_url": "https://i.ibb.co/8D1RrRT3/IMG-20250628-234649.jpg",
        "status": "Ready",
        "category": "JSHook"
    },
    10: {
        "name": "JSHook (ZIVPN)",
        "desc": "exclusive script for decrypt ziv.",
        "price": 15,
        "image_url": "https://i.ibb.co/tNvxJkf/Screenshot-2025-07-06-21-49-46-033-com-vphonegaga-titan.jpg",
        "status": "Ready",
        "category": "JSHook"
    },
    11: {
        "name": "JSHook (SSH Injector)",
        "desc": "exclusive script for decrypt ssh.",
        "price": 10,
        "image_url": "https://i.ibb.co/Ldhvqfbs/Screenshot-2025-07-06-22-13-18-471-com-vphonegaga-titan.jpg",
        "status": "Ready",
        "category": "JSHook"
    },
    12: {
        "name": "JSHook (StarkVPN Reloaded)",
        "desc": "exclusive script for decrypt stk.",
        "price": 10,
        "image_url": "https://i.ibb.co/0Vzv43br/Screenshot-2025-07-08-18-20-27-255-com-vphonegaga-titan.jpg",
        "status": "Ready",
        "category": "JSHook"
    },
    13: {
        "name": "JSHook (NexPrime VPN)",
        "desc": "exclusive script for decrypt nxp.",
        "price": 10,
        "image_url": "https://i.ibb.co/S4wkDS13/Screenshot-2025-07-09-07-27-08-118-com-vphonegaga-titan.jpg",
        "status": "Ready",
        "category": "JSHook"
    },
    14: {
        "name": "JSHook (SBR Injector)",
        "desc": "exclusive script for decrypt sbr.",
        "price": 10,
        "image_url": "https://i.ibb.co/Vcb0VLmQ/IMG-20250709-072932.jpg",
        "status": "Ready",
        "category": "JSHook"
    },
    15: {
        "name": "JSHook (OpenCustom)",
        "desc": "exclusive script for decrypt oc.",
        "price": 10,
        "image_url": "https://i.ibb.co/bRK0P8xx/Screenshot-2025-07-10-22-02-06-606-com-vphonegaga-titan.jpg",
        "status": "Ready",
        "category": "JSHook"
    },
    16: {
        "name": "StarkVPN Reloaded (Server)",
        "desc": "exclusive script for decrypt ??.",
        "price": 20,
        "image_url": "https://i.ibb.co/BV6NR2Ln/Screenshot-2025-07-09-14-18-08-947-com-vphonegaga-titan.jpg",
        "status": "Coming soon",
        "category": "JSHook+Server"
    },
    17: {
        "name": "OpenCustom (Server)",
        "desc": "exclusive script for decrypt ??.",
        "price": 20,
        "image_url": "https://i.ibb.co/pBz32r7q/Screenshot-2025-07-10-22-52-53-979-com-vphonegaga-titan.jpg",
        "status": "Coming soon",
        "category": "JSHook+Server"
    },
    18: {
        "name": "JSHook (?????) Coming soon🔥",
        "desc": "exclusive script for decrypt ??.",
        "price": 99,
        "image_url": "https://i.ibb.co/hFbc0r8v/file-00000000f898622faa3931383e04bb3f.png",
        "status": "Coming soon",
        "category": "JSHook"
    },
}

pending_payment = {}
admin_order_refs = {}

def format_runtime():
    uptime = int(time.time() - start_time)
    hours, remainder = divmod(uptime, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

# Kirim daftar kategori sebagai tombol
def send_category_list(chat_id):
    categories = {}
    for p in products.values():
        cat = p.get("category", "Uncategorized")
        categories[cat] = categories.get(cat, 0) + 1

    msg = "🗂 *Select Product Category :*"
    markup = InlineKeyboardMarkup(row_width=2)
    for cat in categories.keys():
        markup.add(InlineKeyboardButton(cat, callback_data=f"category_{cat}"))
    bot.send_message(chat_id, msg, reply_markup=markup, parse_mode='Markdown')


# Kirim daftar produk dalam kategori
def send_products_by_category(chat_id, category):
    filtered = [(pid, p) for pid, p in products.items() if p.get("category", "") == category]
    if not filtered:
        bot.send_message(chat_id, f"❌ Category *{category}* not found or no product yet.", parse_mode='Markdown')
        return

    msg = f"📦 *Products in the category :* `{category}`\n\n"
    markup = InlineKeyboardMarkup(row_width=1)
    for pid, p in filtered:
        msg += f"▫️ *{p['name']}* - `${p['price']}` ({p['status']})\n"
        markup.add(InlineKeyboardButton(f"🔎 View {p['name']}", callback_data=f"view_{pid}"))
    markup.add(InlineKeyboardButton("🔙 Back to Category", callback_data="back_to_categories"))
    bot.send_message(chat_id, msg, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(commands=['start'])
def handle_start(message):
    now = datetime.datetime.now()
    today = now.strftime("%A, %d %B %Y")
    start_msg = (
        f"👋 *Welcome to the Nathan - STORE!*\n──────────────────────\nThis is your time for be best decryptor. 😈\nYou’ll enjoy use tools from us — stay alert!\n\n_We provide high-quality scripts and tools for decrypting VPN configuration._\n\n📆 *Today* : `{today}`\n⏱ *Bot Runtime* : `{format_runtime()}`\n"
    )
    ping = int((time.time() - time.time()) * 1000)
    start_msg += f"📶 *PING* : `5 ms`\n\n" #{ping}
    categories = {}
    for p in products.values():
        cat = p.get("category", "Uncategorized")
        categories[cat] = categories.get(cat, 0) + 1
    start_msg += "🛍 *Available Categories* :\n"
    for cat, count in categories.items():
        start_msg += f"• `{cat} (Total : {count})`\n"
    start_msg += "\nUse /menu to view products.\nUse /free to claim a gift 🎁 (free script random)\n──────────────────────\n© Nathan | @NathanaeruCH"
    bot.send_message(message.chat.id, start_msg, parse_mode='Markdown')

@bot.message_handler(commands=['menu'])
def handle_menu(message):
    send_category_list(message.chat.id)

@bot.message_handler(commands=["free"])
def handle_free(message):
    bot.reply_to(
        message,
        "There is a special gift from someone for you :\n===========❤️🐣❤️===========\nThanks to @Leneath"
    )
    gift_path = os.path.join(os.getcwd(), "LinkLayerVPN.lua")
    if os.path.exists(gift_path):
        with open(gift_path, "rb") as gift:
            bot.send_document(message.chat.id, gift, caption="────────────────\n• Target : LinkLayer VPN\n• Extension : .Ink\nType : Auto Print Lua ✅")
    else:
        bot.send_message(message.chat.id, "❌ Gift file not found.")

@bot.message_handler(commands=['cancel'])
def cancel(message):
    chat_id = message.chat.id
    if chat_id in pending_payment:
        pending_payment.pop(chat_id)
        bot.send_message(chat_id, "❌ Your order has been canceled.")
    else:
        bot.send_message(chat_id, "You don't have any active order.")

@bot.callback_query_handler(func=lambda call: True)
def handle_buttons(call):
    chat_id = call.message.chat.id
    data = call.data

    if data.startswith("category_"):
        category = data[len("category_"):]
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass
        send_products_by_category(chat_id, category)

    elif data == "back_to_categories":
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass
        send_category_list(chat_id)

    elif data.startswith("view_"):
        pid = int(data.split("_")[1])
        p = products[pid]
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass
        caption = (
            f"╭─────────────────╮\n│ *Product ID :* `{pid}`\n"
            f"│ *Name :* `{p['name']}`\n"
            f"│ *Description :* \n│ _{p['desc']}_\n├──────────────────\n"
            f"│ 💵 *Price :* `${p['price']}`\n"
            f"│ 📦 *Status :* `{p['status']}`\n╰─────────────────╯"
        )
        markup = InlineKeyboardMarkup(row_width=2)
        if p['status'].lower() == "ready":
            markup.add(
                InlineKeyboardButton("💳 Buy Now", callback_data=f"buy_{pid}"),
                InlineKeyboardButton("🔙 Back to Products", callback_data=f"back_to_products_{p['category']}")
            )
        else:
            markup.add(
                InlineKeyboardButton("🔙 Back to Products", callback_data=f"back_to_products_{p['category']}")
            )
        bot.send_photo(chat_id, p['image_url'], caption=caption, parse_mode='Markdown', reply_markup=markup)

    elif data.startswith("back_to_products_"):
        category = data[len("back_to_products_"):]
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass
        send_products_by_category(chat_id, category)

    elif data.startswith("buy_"):
        pid = int(data.split("_")[1])
        p = products[pid]
        pending_payment[chat_id] = {"pid": pid, "product": p}
        instruction = (
            f"╭─────────────────╮\n│ 🧾 *Purchase :* `{p['name']}`\n"
            f"│ 💰 *Price :* `${p['price']}`\n╰─────────────────╯\n"
            f"📌 *Payment Instructions:*\n"
            f"☕ Donate via ko-fi : [Nathanaeru](https://ko-fi.com/nathanaeru#checkoutModal)\n"
            f"💳 Pay via Paypal : [Nathanaeru Gateway](https://www.paypal.me/imlutfifarid)\n"
        )
        for name, wallet in CRYPTO_WALLET.items():
            instruction += f"🪙 Pay via {name} : `{wallet}`\n"
        instruction += (
            "\n📤 Please *send a photo* of your payment proof.\n"
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
    if chat_id not in pending_payment:
        bot.send_message(chat_id, "❗ You have no active order. Use /menu to start shopping.")
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
        f"📥 *Payment Proof Received*\n"
        f"🛒 Product: {p['name']}\n"
        f"💵 Price: ${p['price']}\n"
        f"👤 Buyer: {full_name}\n"
        f"👤 Username: @{user_aidi}\n"
        f"🆔 Ref ID: {ref_id}"
    )
    bot.send_photo(ADMIN_CHAT_ID, message.photo[-1].file_id, caption=caption, parse_mode='Markdown')
    bot.send_message(chat_id, "✅ Your payment proof has been submitted. Please wait for confirmation.")
    pending_payment.pop(chat_id)

@bot.message_handler(content_types=['document', 'text'], func=lambda msg: msg.reply_to_message and msg.chat.id == ADMIN_CHAT_ID)
def handle_admin_reply(msg):
    reply = msg.reply_to_message
    if not reply.caption or "Ref ID:" not in reply.caption:
        bot.send_message(ADMIN_CHAT_ID, "⚠️ Please reply to a valid payment proof message containing a Ref ID.")
        return
    try:
        ref_id_line = [line for line in reply.caption.splitlines() if "Ref ID:" in line][0]
        ref_id = ref_id_line.split(":")[-1].strip()
        order = admin_order_refs.get(ref_id)
        if not order:
            bot.send_message(ADMIN_CHAT_ID, "❌ Reference ID not found.")
            return
        buyer_id = order["buyer_id"]
        chat_id = order["chat_id"]
        instruction_msg_id = order.get("instruction_msg_id")
        if msg.content_type == "document":
            bot.send_document(buyer_id, msg.document.file_id, caption="📦 Here is your order. Thank you!")
        else:
            bot.send_message(buyer_id, f"Nathan Payment API System :\n{msg.text}\n──────────────────")
        if instruction_msg_id:
            try:
                bot.delete_message(chat_id, instruction_msg_id)
            except:
                pass
        bot.send_message(ADMIN_CHAT_ID, f"✅ Sent to buyer ID `{buyer_id}`", parse_mode='Markdown')
        del admin_order_refs[ref_id]
    except Exception as e:
        bot.send_message(ADMIN_CHAT_ID, f"❌ Error: {e}")

@app.route('/')
def index():
    return render_template('index.html', products=products)

def start_bot():
    bot.polling(non_stop=True)

if __name__ == '__main__':
    threading.Thread(target=start_bot).start()
    app.run(host='0.0.0.0', port=5000)