import os
import telebot
from telebot import types
from dotenv import load_dotenv

# Mengambil token dari Environment Variable
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

ADMIN_USERNAME = "pikipurwanto"
TRADE_LINK = "LINK_MINI_APPS_KAMU"
FREE_SIGNAL_LINK = "https://t.me/pejuang_daytrading"
QRIS_IMAGE = "QRPDTFX.PNG"

# Validasi jika token tidak ditemukan
if not TOKEN:
    raise ValueError("Error: TELEGRAM_BOT_TOKEN tidak ditemukan di Environment Variables!")

bot = telebot.TeleBot(TOKEN)

# ... (sisa kode kamu ke bawahnya TETAP SAMA, tidak perlu diubah)
