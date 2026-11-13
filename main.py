import telebot
from telebot import types
import json
import os

TOKEN = "8563857504:AAEXxVc25EEmTRcLdgIx8JejaT4Tpm2bIao"
bot = telebot.TeleBot(TOKEN)

FILE = "users.json"

def load_users():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    with open(FILE, "w") as f:
        json.dump(users, f)

def get_user(user_id):
    users = load_users()
    uid = str(user_id)
    if uid not in users:
        users[uid] = {'balance': 200, 'taps': 0}
        save_users(users)
    return users[uid]

def update_user(user_id, balance, taps):
    users = load_users()
    users[str(user_id)] = {'balance': balance, 'taps': taps}
    save_users(users)

def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👆 TAP +10", callback_data="tap"),
        types.InlineKeyboardButton("💰 BALANCE", callback_data="balance"),
        types.InlineKeyboardButton("🎮 PLAY TAPCASH ARENA", callback_data="play")
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user = get_user(message.from_user.id)
    name = message.from_user.first_name
    bot.send_message(message.chat.id, f"👋 Welcome {name} to TapCash Arena!\n\n💰 Balance: {user['balance']} coins\n👆 Taps: {user['taps']}\n\nPress TAP +10 to earn!", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def handle_button(call):
    user = get_user(call.from_user.id)
    name = call.from_user.first_name
    if call.data == "tap":
        user['balance'] += 10
        user['taps'] += 1
        update_user(call.from_user.id, user['balance'], user['taps'])
        try:
            bot.answer_callback_query(call.id, " +10 coins! 🎉")
        except:
            pass
        text = f"👋 Welcome {name} to TapCash Arena!\n\n💰 Balance: {user['balance']} coins\n👆 Taps: {user['taps']}\n\nYou tapped! +10 coins added!"
    elif call.data == "balance":
        text = f"💰 Your Balance: {user['balance']} coins\n👆 Total Taps: {user['taps']}"
    elif call.data == "play":
        text = f"🎮 TAPCASH ARENA - GAME MODE 🎮\n\n👋 {name}, you are IN the Arena now!\n\n💰 Balance: {user['balance']} coins\n👆 Taps: {user['taps']}\n\n⚡ TAP AS FAST AS YOU CAN!"
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    except:
        pass

print("TapCash Arena Bot is running...")
bot.infinity_polling()