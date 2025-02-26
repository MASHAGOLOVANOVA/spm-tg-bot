from telegram.constants import ParseMode

from bot.bot import bot
from meeting.meeting_service import *
from datetime import datetime, timedelta
import telebot
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


def handle_meeting_name(message, project_id, student_id):
    """функция для получения названия встречи"""
    name = message.text  # Получаем название

    bot.send_message(message.chat.id, "Введите описание встречи:")
    bot.register_next_step_handler(
        message, handle_meeting_description, project_id, student_id, name
    )


def handle_meeting_description(message, project_id, student_id, name):
    """функция для получения описания встречи"""
    desc = message.text  # Получаем название

    bot.send_message(message.chat.id, "Введите время встречи:")
    bot.register_next_step_handler(
        message, handle_meeting_time, project_id, student_id, name, desc
    )


def handle_meeting_time(message, project_id, student_id, name, desc):
    """функция для получения времени встречи"""
    time = message.text  # Получаем название встречи

    bot.send_message(
        message.chat.id,
        "Выберите формат встречи:",
        reply_markup=get_meeting_format_markup(),
    )
    meeting_options = {"name": name, "desc": desc}
    bot.register_next_step_handler(
        message, handle_meeting_format, project_id, student_id, meeting_options, time
    )


def get_meeting_format_markup():
    """функция для получения доски для выбора формата встречи"""
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button_online = telebot.types.KeyboardButton("Онлайн")
    button_offline = telebot.types.KeyboardButton("Оффлайн")
    markup.add(button_online, button_offline)
    return markup


def handle_meeting_format(message, project_id, student_id, meeting_options, time):
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
        iso_time = (datetime.strptime(time, "%d.%m.%Y %H:%M")).isoformat()

        # Формируем данные для новой встречи
        new_meeting_data = {
            "name": meeting_options["name"],
            "description": meeting_options["desc"],
            "project_id": int(project_id),
            "student_participant_id": int(student_id),
            "is_online": online,
            "meeting_time": iso_time + "Z",  # Преобразуем в строку ISO 8601
        }

        # Отправляем запрос на создание встречи
        if add_meeting(new_meeting_data):
            bot.send_message(message.chat.id, "Встреча успешно добавлена!")

    except ValueError:
        bot.send_message(
            message.chat.id,
            "Неверный формат даты. Пожалуйста, используйте формат YYYY-MM-DD HH:MM.",
        )
    except Exception as e:
        bot.send_message(message.chat.id, str(e))
    finally:
        show_main_menu(message.chat.id)
