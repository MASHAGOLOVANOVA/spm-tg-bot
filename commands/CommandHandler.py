from bot.bot import bot
import telebot


@bot.message_handler(commands=["start"])
def start_message(message):
    """Хендлер команды start"""
    # Создаем кнопку для запроса номера телефона
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button = telebot.types.KeyboardButton("Отправить номер телефона", request_contact=True)
    keyboard.add(button)

    bot.send_message(
        message.chat.id,
        """Привет! \n
Это бот Системы для управления студенческими проектами!
Пожалуйста, отправьте свой номер телефона.""",
        reply_markup=keyboard,
    )
