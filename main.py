import wikipedia
wikipedia.set_lang('uz')
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


# 🔹 Bot tokenini shu yerga kiriting
TOKEN = "8133713557:AAHrt3h8wsPWrQ6zqk7dyJoesC4_UoWykUo"
bot = telebot.TeleBot(TOKEN)
bot.set_my_description("🤖 Salom! Men mavzular uchun maqola botiman.\n"
                       "📝 /start tugmasini bosing!\n"
                       "🔹 Matn kiriting va men maqola chiqaraman")


# 🔹 Foydalanuvchiga asosiy tugmalarni beruvchi funksiya
def main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton("📜 Matn kiritish"))
    keyboard.row(KeyboardButton("ℹ️ Ma’lumot"))
    return  keyboard


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
        bot.send_message(message.chat.id, f"Matn kiritish' tugmasini bosdingiz. Iltimos, matn kiriting:",reply_markup = ReplyKeyboardRemove())

    elif message == "ℹ️ Ma’lumot":
        bot.send_message(message.chat.id, f"Bu bot sizga matn kiritish va ma’lumot olish imkonini beradi.",reply_markup = ReplyKeyboardRemove())
    else:
        try:
            out = wikipedia.summary(message.text)
        except:
            bot.send_message(message.chat.id, f"😔😔😔 Afsuski Bunday maqola topilmadi")
        else:
            bot.send_message(message.chat.id, f"{out}")






# 🔹 Botni ishga tushirish
print("Bot ishga tushdi...")
bot.polling(none_stop=True)
