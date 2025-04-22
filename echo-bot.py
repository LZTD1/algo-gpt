import telebot # <- Импорт скачанного модуля

BOT_TOKEN = 'TOKEN' # <- Здесь указываем свой телеграм токен из BotFather
bot = telebot.TeleBot(BOT_TOKEN) # <- Создаем обьект телеграм бота

@bot.message_handler(func=lambda message: True) # <- Регистрируем обработчик события "на сообщение"
def echo_all(message): # <- Тогда будет выполнена функция "echo_all"
    bot.send_message(message.chat.id, message.text) 
    #                   ^^^
    # Которая просто отошлет наш же текст "message.text",
    # нам же (наш ID) "message.chat.id"

bot.polling() # <- Старт бота
