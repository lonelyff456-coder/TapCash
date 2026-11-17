import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import telebot
from telebot import types

# --- Keep Render Web Service alive - serves index.html ---
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with open("index.html", "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content)
        except:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"TapCash Bot is running!")
    def log_message(self, format, *args):
        pass

def run_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# --- Bot - SAFE, token from Environment ---
TOKEN = os.environ.get("BOT_TOKEN", "")
WEBAPP_URL = os.environ.get("WEBAPP_URL", "https://tapcash-2.onrender.com")

bot = telebot.TeleBot(TOKEN)

# All game progress is inside WebApp only

def main_menu():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🎮 PLAY TAPCASH ARENA", web_app=types.WebAppInfo(url=WEBAPP_URL))
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name
    text = f"Welcome {name} to TapCash Arena! 🎮\n\n"
    text += "Play the tapping game, collect Coins, unlock new levels and get bonus Energy.\n\n"
    text += "Tap, play and have fun with friends!\n\n"
    text += "Press PLAY below to open the game 👇"
    bot.send_message(message.chat.id, text, reply_markup=main_menu())

@bot.message_handler(commands=['privacy'])
def privacy(message):
    text = "TapCash Arena Privacy Policy:\n\n"
    text += "We only use your Telegram ID to save your game progress and score. "
    text += "We do not collect your password, phone number or private messages."
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['about'])
def about(message):
    text = "About TapCash Arena:\n\n"
    text += "TapCash Arena is a fun tapping game. Play, level up, collect
