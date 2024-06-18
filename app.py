import telebot
from time import sleep

admin = 5818477287
bot = telebot.TeleBot("6997709623:AAGkUOQb9Cyjxx3uKrKdZY6a3iyfl2nejzM")

# حذف الـ Webhook
bot.remove_webhook()

@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.reply_to(message, "اهلًا بك في بوت التواصل، ارسل رسالتك.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.from_user.id != admin:
        bot.forward_message(admin, message.chat.id, message.message_id)
        sleep(1)
        bot.reply_to(message, "تم ارسال رسالتك، سيقوم مالك البوت بالرد عليك في أقرب وقت.")
    elif message.reply_to_message and message.reply_to_message.forward_from and message.from_user.id == admin:
        id = message.reply_to_message.forward_from.id
        bot.send_message(id, message.text)
        sleep(1)
        bot.reply_to(message, "تم ارسال رسالتك للشخص.")

# بدء الـ polling
bot.infinity_polling()
