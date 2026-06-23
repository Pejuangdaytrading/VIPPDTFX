import os
import telebot
from telebot import types, apihelper
from dotenv import load_dotenv

# Mengatur path absolut ke folder project agar file .env & gambar pasti terbaca
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Mengambil token dari Environment Variable (.env)
load_dotenv(os.path.join(BASE_DIR, ".env"))
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# 2. SETTING PROXY UTK AKUN GRATIS PYTHONANYWHERE
apihelper.proxy = {'https': 'http://proxy.server:3128'}

# 3. KONFIGURASI VARIABEL
ADMIN_USERNAME = "pikipurwanto"
TRADE_LINK = "https://one.exnessonelink.com/a/trvppueskc" # Silakan ganti dengan link Mini Apps asli kamu
FREE_SIGNAL_LINK = "https://t.me/pejuang_daytrading"
QRIS_IMAGE = os.path.join(BASE_DIR, "QRPDTFX.PNG") 

# Validasi jika token gagal dimuat
if not TOKEN:
    # Jika gagal membaca .env, kita buat log error khusus ke nohup.out
    print("CRITICAL ERROR: TELEGRAM_BOT_TOKEN tidak terbaca di file .env!")
    exit(1)

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🚀 Trade Now", url=TRADE_LINK))
    markup.add(types.InlineKeyboardButton("📘 Panduan", callback_data="panduan"))
    markup.add(types.InlineKeyboardButton("💎 Join VIP Channel", callback_data="vip"))
    markup.add(types.InlineKeyboardButton("👤 Chat Admin", url=f"https://t.me/{ADMIN_USERNAME}"))
    markup.add(types.InlineKeyboardButton("📡 Free Signal PDT Fx", url=FREE_SIGNAL_LINK))

    text = (
        "🚀 Selamat datang di PDT Fx\n\n"
        "Akses signal Gold + strategi trading harian.\n\n"
        "Pilih menu di bawah:"
    )
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(commands=['admin'])
def admin(message):
    bot.reply_to(message, f"Chat admin @{ADMIN_USERNAME}")


@bot.message_handler(commands=['panduan'])
def panduan_command(message):
    send_panduan(message.chat.id)


@bot.message_handler(commands=['vip'])
def vip_command(message):
    send_vip(message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data in ["panduan", "vip"])
def button_handler(call):
    bot.answer_callback_query(call.id)
    if call.data == "panduan":
        send_panduan(call.message.chat.id)
    elif call.data == "vip":
        send_vip(call.message.chat.id)


def send_panduan(chat_id):
    text = (
        "🚀 Mulai Trading Bareng PDT Fx\n\n"
        "1️⃣ Klik tombol Trade Now\n"
        "👉 Register di broker rekomendasi yang muncul pada mini apps.\n\n"
        "2️⃣ Setelah akun trading jadi\n"
        f"👉 Chat admin @{ADMIN_USERNAME}\n"
        "👉 Kirim nomor akun trading kamu.\n\n"
        "🔒 Tujuan:\n"
        "Untuk validasi bahwa kamu register melalui link resmi PDT Fx.\n\n"
        "⚠️ Tanpa validasi, akses signal VIP tidak diberikan.\n\n"
        "Klik Trade Now sekarang dan lanjutkan prosesnya 🔥"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🚀 Trade Now", url=TRADE_LINK))
    markup.add(types.InlineKeyboardButton("👤 Chat Admin", url=f"https://t.me/{ADMIN_USERNAME}"))
    markup.add(types.InlineKeyboardButton("📡 Free Signal", url=FREE_SIGNAL_LINK))
    bot.send_message(chat_id, text, reply_markup=markup)


def send_vip(chat_id):
    text = (
        "💎 Join VIP Channel PDT Fx\n\n"
        "Dapatkan akses signal Gold VIP, market update, dan insight trading eksklusif.\n\n"
        "💳 Harga VIP\n"
        "• Rp150.000 / month\n"
        "• Rp1.000.000 Lifetime Access\n\n"
        "📲 Pembayaran via QRIS\n"
        "Silakan scan QRIS pada gambar ini menggunakan e-wallet / mobile banking.\n\n"
        "📩 Setelah pembayaran:\n"
        f"👉 Chat admin @{ADMIN_USERNAME}\n"
        "👉 Kirim bukti pembayaran\n\n"
        "⚠️ Akses VIP diberikan setelah pembayaran dikonfirmasi."
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("👤 Konfirmasi Pembayaran", url=f"https://t.me/{ADMIN_USERNAME}"))

    try:
        with open(QRIS_IMAGE, "rb") as photo:
            bot.send_photo(chat_id, photo, caption=text, reply_markup=markup)
    except FileNotFoundError:
        bot.send_message(chat_id, text + "\n\n_(Gagal memuat gambar QRIS, silakan hubungi admin)_", reply_markup=markup)


# Menjalankan mesin polling bot
print("Bot sedang berjalan...")
bot.infinity_polling(skip_pending=True, timeout=20, long_polling_timeout=20)
