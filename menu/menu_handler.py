from bot.bot import bot, CLIENT_URL
import telebot.types
from integration.integration_handler import get_google_planner


def show_main_menu(chat_id):
    """функция открытия главного меню"""
    # Создаем главное меню
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_projects = telebot.types.KeyboardButton("Мои проекты")
    button_meetings = telebot.types.KeyboardButton("Мои встречи")
    button_add_project = telebot.types.KeyboardButton("Добавить проект")  # Новая кнопка

    has_planner = get_google_planner()
    if has_planner is not None:
        keyboard.add(button_projects, button_meetings, button_add_project)
    else:
        bot.send_message(
            chat_id,
            f"""К сожалению Вам недоступно расписание встреч!\n
Чтобы пользоваться расписанием, подключите Google Calendar из веб-приложения:
\n{CLIENT_URL}/profile/integrations""",
        )
        keyboard.add(button_projects, button_add_project)

    bot.send_message(chat_id, "Выберите действие:", reply_markup=keyboard)
