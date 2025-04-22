import telebot

# Start keyboard
start = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
image_button = telebot.types.KeyboardButton(text="Фото 🖼")
text_button = telebot.types.KeyboardButton(text="Текст 📝")
start.add(image_button, text_button)

# Back keyboard
back = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
back_button = telebot.types.KeyboardButton(text="◀️ В меню")
back.add(back_button)
