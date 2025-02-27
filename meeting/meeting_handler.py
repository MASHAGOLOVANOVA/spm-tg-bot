"""
meeting-handler - Модуль для обработки встреч пользователя
"""
from datetime import timedelta, datetime
import telebot
from telegram.constants import ParseMode

from meeting.meeting_service import get_meetings, add_meeting
from menu.menu_handler import show_main_menu

days_translation = {
    "Monday": "Понедельник",
    "Tuesday": "Вторник",
    "Wednesday": "Среда",
    "Thursday": "Четверг",
    "Friday": "Пятница",
    "Saturday": "Суббота",
    "Sunday": "Воскресенье",
}


def meeting_handler_init(bot):
    """Хендлер init"""

    @bot.message_handler(func=lambda message: message.text == "Мои встречи")
    def handle_meetings(message):
        """Хендлер встреч"""
        meetings = get_meetings()
        if len(meetings) > 0:
            response = format_meetings(group_meetings_by_day(meetings))
            for d in response:
                bot.send_message(message.chat.id, d, parse_mode=ParseMode.MARKDOWN)
        else:
            bot.send_message(message.chat.id, "Встречи не назначены")

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith("add_meeting_project_")
    )
    def handle_project_new_meeting(call):
        """Хендлер для добавления встречи по проекту"""
        project_id = call.data.split("_")[3]
        student_id = call.data.split("_")[5]

        bot.send_message(call.message.chat.id, "Введите название встречи:")
        bot.register_next_step_handler(
            call.message, handle_meeting_name, project_id, student_id
        )


def handle_meeting_name(bot, message, project_id, student_id):
    """функция для получения названия встречи"""
    name = message.text  # Получаем название

    bot.send_message(message.chat.id, "Введите описание встречи:")
    bot.register_next_step_handler(
        bot, message, handle_meeting_description, project_id, student_id, name
    )


def handle_meeting_description(bot, message, project_id, student_id, name):
    """функция для получения описания встречи"""
    desc = message.text  # Получаем название
    meeting_info = {
        "name": name,
        "description": desc,
        "project_id": project_id,
        "student_id": student_id
    }
    bot.send_message(message.chat.id, "Введите время встречи:")
    bot.register_next_step_handler(
        message, handle_meeting_time, meeting_info
    )


def handle_meeting_time(bot, message, meeting_info):
    """функция для получения времени встречи"""
    time = message.text
    try:
        iso_time = (datetime.strptime(time, "%d.%m.%Y %H:%M")).isoformat()
        meeting_info["start_time"] = iso_time
        bot.send_message(
            message.chat.id,
            "Выберите формат встречи:",
            reply_markup=get_meeting_format_markup(),
        )
        bot.register_next_step_handler(
            bot, message, handle_meeting_format, meeting_info
        )
    except ValueError:
        bot.send_message(
            message.chat.id,
            "Неверный формат даты. Пожалуйста, используйте формат YYYY-MM-DD HH:MM.",
        )
        bot.register_next_step_handler(
            bot, message, handle_meeting_time, meeting_info
        )


def handle_meeting_format(bot, message, meeting_info):
    """Функция для получения формата встречи."""
    meeting_format = message.text  # Получаем формат встречи

    if meeting_format not in ["Онлайн", "Оффлайн"]:
        bot.send_message(
            message.chat.id,
            "Пожалуйста, выберите корректный формат встречи: Онлайн или Оффлайн.",
        )
        return  # Завершаем выполнение функции, если формат некорректный

    try:
        online = meeting_format == "Онлайн"  # Устанавливаем значение is_online
        # Формируем данные для новой встречи
        new_meeting_data = {
            "name": meeting_info["name"],
            "description": meeting_info["desc"],
            "project_id": int(meeting_info["project_id"]),
            "student_participant_id": int(meeting_info["student_id"]),
            "is_online": online,
            "meeting_time": meeting_info["time"] + "Z",  # Преобразуем в строку ISO 8601
        }

        # Отправляем запрос на создание встречи
        if add_meeting(new_meeting_data):
            bot.send_message(message.chat.id, "Встреча успешно добавлена!")

    except ValueError:
        bot.send_message(
            message.chat.id,
            "Неверный формат даты. Пожалуйста, используйте формат YYYY-MM-DD HH:MM.",
        )
    finally:
        show_main_menu(message.chat.id)


def get_meeting_format_markup():
    """функция для получения доски для выбора формата встречи"""
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button_online = telebot.types.KeyboardButton("Онлайн")
    button_offline = telebot.types.KeyboardButton("Оффлайн")
    markup.add(button_online, button_offline)
    return markup


def group_meetings_by_day(meetings):
    """функция для группировки встреч"""
    grouped = {}
    for meeting in meetings:
        meeting_time = datetime.fromisoformat(meeting["time"].replace("Z", "+00:00"))
        day = days_translation.get(meeting_time.strftime("%A"))  # Получаем день недели
        date = meeting_time.strftime("%d.%m.%Y")
        day += f", {date}"
        if day not in grouped:
            grouped[day] = []
        grouped[day].append(meeting)
    return grouped


def format_meetings(grouped_meetings):
    """функция для форматирования встреч"""
    alldays = []
    for day, meetings in grouped_meetings.items():
        response = f"*{day}*\n\n"  # Заголовок дня недели
        for meeting in meetings:
            start_time = datetime.fromisoformat(meeting["time"].replace("Z", "+00:00"))
            end_time = start_time + timedelta(
                hours=1
            )  # Добавляем 1 час к начальному времени

            # Форматируем время
            formatted_start_time = start_time.strftime("%H:%M")
            formatted_end_time = end_time.strftime("%H:%M")
            response += f"{formatted_start_time}"
            response += f" - {formatted_end_time}\nНазвание: {meeting['name']}\n"
            response += f"Описание: {meeting['description']}\n"
            response += f"Студент: {meeting['student']['name']},"
            response += f" Курс: {meeting['student']['cource']}\n"
            response += f"{'Онлайн' if meeting['is_online'] else 'Оффлайн'}\n\n"
        response += "\n"
        alldays.append(response)
    return alldays
