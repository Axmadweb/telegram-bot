import wikipedia
import os
import threading
import schedule
import time

from flask import Flask, request
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Wikipedia tilini O'zbek tiliga sozlash
wikipedia.set_lang('uz')

# Bot tokenini atrof-muhit o'zgaruvchisidan olish
TOKEN = os.getenv("8133713557:AAHrt3h8wsPWrQ6zqk7dyJoesC4_UoWykUo")
if not TOKEN:
    raise ValueError("Bot tokeni yo'q! Iltimos, atrof-muhit o'zgaruvchisida TOKEN ni belgilang.")

bot = telebot.TeleBot(TOKEN)

# Flask ilovasini yaratish
app = Flask(__name__)

# 🔹 Tugmalarni yaratish
def main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton("📜 Matn kiritish"))
    keyboard.row(KeyboardButton("ℹ️ Ma’lumot"))
    return keyboard

# 🔹 /start komandasi
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Assalomu alaykum! Men sizning Telegram botingizman! 😊", reply_markup=main_menu())

# 🔹 /menu komandasi
@bot.message_handler(commands=['menu'])
def menu_handler(message):
    bot.send_message(message.chat.id, "Kerakli bo‘limni tanlang:", reply_markup=main_menu())

# 🔹 Kanalga rejalashtirilgan xabarni yuborish
CHANNEL_USERNAME = "@deom_for_python"
IMAGE_PATH = "image.png"

def send_scheduled_message():
    message = """<b>🌙 HAYIT MUBORAK! 🌙</b>\n
Salom, Quanta oilasi! ⚡\n
Bugun nafaqat yangi kun, balki yangi imkoniyatlar, yorqin kelajak va mehr ulashish vaqti!\n
<b>🌙 Hayit ayyomingiz muborak bo‘lsin!</b>\n
💡 Texnologiya, ilm-fan va kreativ dunyoda olg‘a intilayotgan barchangizga muvaffaqiyat tilaymiz!\n
<b>Quanta bilan yorqin kelajakka birga qadam qo‘yaylik! 🚀</b>
"""
    with open(IMAGE_PATH, "rb") as photo:
        bot.send_photo(CHANNEL_USERNAME, photo, caption=message, parse_mode="HTML")

# Har kuni 00:00 da xabar yuborish
schedule.every().day.at("23:03").do(send_scheduled_message)

def schedule_runner():
    while True:
        schedule.run_pending()
        time.sleep(30)

# 🔹 Matnni qabul qilish va Wikipedia'dan ma'lumot olish
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "📜 Matn kiritish":
        bot.send_message(message.chat.id, "Iltimos, matn kiriting:", reply_markup=ReplyKeyboardRemove())
    elif message.text == "ℹ️ Ma’lumot":
        bot.send_message(message.chat.id, "Bu bot Wikipedia'dan ma'lumot topib beruvchi bot.", reply_markup=ReplyKeyboardRemove())
    else:
        try:
            out = wikipedia.summary(message.text, sentences=2)
            bot.send_message(message.chat.id, f"{out}")
        except wikipedia.exceptions.DisambiguationError as e:
            options = "\n".join(e.options[:5])
            bot.send_message(message.chat.id, f"😔 Bir nechta maqolalar topildi. Aniqroq matn kiriting:\n{options}")
        except wikipedia.exceptions.PageError:
            bot.send_message(message.chat.id, "😔 Maqola topilmadi.")
        except Exception as e:
            bot.send_message(message.chat.id, f"😔 Xatolik: {str(e)}")

# 🔹 Webhook uchun endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

# 🔹 Flask serverini ishga tushirish
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://telegram-bot-8unt.onrender.com/webhook")

    # Jadval bajaruvchi threadni ishga tushirish
    threading.Thread(target=schedule_runner, daemon=True).start()

    # Flask serverini ishga tushirish
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
