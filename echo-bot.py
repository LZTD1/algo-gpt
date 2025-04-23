import telebot
import keyboards
import fsm
import ai
import loguru
import yaml
import sys

logger = loguru.logger

# load config
try:
    with open("./config.yaml", 'r') as file: # Здесь, за исключением доп. нагрузки, сделаем 
        # Захардкоженный путь до конфига
        cfg = yaml.safe_load(file)
        logger.info("Успешно загружен конфиг")
except Exception as e:
    logger.warning("Произошла ошибка при загрузке конфига ({})", str(e))
    sys.exit(1) # Добавим системный выход из приложения

BOT_TOKEN = cfg['telegram_token']
stater = fsm.FSM()
ai_service = ai.AI(cfg)
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)


def handle_default_state(message):
    if message.text == "Фото 🖼":
        stater.set_state(message.chat.id, fsm.IMAGE_STATE)
        bot.send_message(message.chat.id, "Напиши описание фото", reply_markup=keyboards.back)
    elif message.text == "Текст 📝":
        stater.set_state(message.chat.id, fsm.TEXT_STATE)
        bot.send_message(message.chat.id, "Напиши то, о чем ты хочешь меня спросить", reply_markup=keyboards.back)
    else:
        return_to_menu(message.chat.id)

def handle_image_state(message):
    if message.text == "◀️ В меню":
        return_to_menu(message.chat.id)
    else:
        try:
            msg = bot.send_message(chat_id=message.chat.id, text="Генерирую...")
            image_url = ai_service.generate_image(message.text)
            bot.delete_message(chat_id=message.chat.id, message_id=msg.id)
            bot.send_photo(chat_id=message.chat.id, caption="Ваше фото:", photo=image_url)
        except Exception as e:
            bot.send_message(chat_id=message.chat.id, text=f"Произошла ошибка ({str(e)})")

def handle_text_state(message):
    if message.text == "◀️ В меню":
        ai_service.clear_dialog(message.chat.id)
        return_to_menu(message.chat.id)
    else:
        msg = bot.send_message(message.chat.id, "Думаю над запросом ...")
        txt = ai_service.generate_text(message.text, message.chat.id)
        msg = bot.edit_message_text(text=txt, chat_id=message.chat.id, message_id=msg.id)

def return_to_menu(chat_id):
    stater.set_state(chat_id, fsm.DEFAULT_STATE)
    bot.send_message(chat_id, "Главное меню:", reply_markup=keyboards.start)

@bot.message_handler(func=lambda message: True) 
def on_message(message): 
    state = stater.get_state(message.chat.id)

    logger.info(
        "Пользователь [{}:{}] отправил сообщение '{}' в состоянии {}",
        message.chat.id,
        message.from_user.first_name, 
        message.text,
        state 
    )
    if state == fsm.DEFAULT_STATE:
        handle_default_state(message)
    elif state == fsm.IMAGE_STATE:
        handle_image_state(message)
    elif state == fsm.TEXT_STATE:
        handle_text_state(message)
    else:
        return_to_menu(message.chat.id)
    
bot.polling()