import wikipedia
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import telebot
from flask import Flask, request

# 🔹 Bot tokenini shu yerga kiriting
TOKEN = "8133713557:AAHrt3h8wsPWrQ6zqk7dyJoesC4_UoWykUo"
bot = telebot.TeleBot(TOKEN)
bot.set_my_description("🤖 Salom! Men mavzular uchun maqola botiman.\n"
                       "📝 /start tugmasini bosing!\n"
                       "🔹 Matn kiriting va men maqola chiqaraman")

# Portni olish (Render platformasi uchun)
PORT = os.getenv("PORT", 5000)  # Standart port 5000 bo'lishi mumkin

# Flask ilovasini yaratish
app = Flask(__name__)

# 🔹 Foydalanuvchiga asosiy tugmalarni beruvchi funksiya
def main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton("📜 Matn kiritish"))
    keyboard.row(KeyboardButton("ℹ️ Ma’lumot"))
    return keyboard


# 🔹 /start komandasi uchun handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Assalomu alaykum! Men sizning Telegram botingizman! 😊", reply_markup=main_menu())


# 🔹 /menu komandasi uchun handler
@bot.message_handler(commands=['menu'])
def menu_handler(message):
    bot.send_message(message.chat.id, "Kerakli bo‘limni tanlang:", reply_markup=main_menu())


# 🔹 Matnli xabarlarni qabul qilish
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "📜 Matn kiritish":
        bot.send_message(message.chat.id, f"Matn kiritish' tugmasini bosdingiz. Iltimos, matn kiriting:", reply_markup=ReplyKeyboardRemove())

    elif message.text == "ℹ️ Ma’lumot":
        bot.send_message(message.chat.id, f"Bu bot sizga matn kiritish va ma’lumot olish imkonini beradi.", reply_markup=ReplyKeyboardRemove())
    else:
        try:
            out = wikipedia.summary(message.text)
            bot.send_message(message.chat.id, f"{out}")
        except wikipedia.exceptions.DisambiguationError as e:
            bot.send_message(message.chat.id, f"😔 Afsuski, bir nechta maqolalar topildi. Iltimos, aniqroq matn kiriting.\n\n{e.options}")
        except wikipedia.exceptions.HTTPTimeoutError:
            bot.send_message(message.chat.id, "🌐 Internet aloqasi o'rnatishda muammo yuz berdi. Iltimos, qayta urinib ko'ring.")
        except wikipedia.exceptions.RedirectError:
            bot.send_message(message.chat.id, "😔 Maqola topilmadi. Iltimos, qayta urinib ko'ring.")
        except Exception as e:
            bot.send_message(message.chat.id, f"😔😔😔 Afsuski Bunday maqola topilmadi. Xatolik: {str(e)}")


# 🔹 Webhook endpointi
@app.route("/webhook", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

# Flaskni ishga tushirish
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://telegram-bot-8unt.onrender.com/webhook")
    app.run(host='0.0.0.0', port=PORT)
