"""
meeting_service - Модуль для работы сс встречами

Этот модуль работает с API
"""
from datetime import datetime
from bot.bot import HOST_URL, sessionManager
import requests


def get_meetings():
    """функция для получения расписания"""
    current_time = datetime.utcnow()
    start_of_day = current_time.replace(hour=0, minute=0, second=0, microsecond=0)

    iso_format_time = start_of_day.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    # Формируем URL с параметром from
    url = f"{HOST_URL}/api/v1/meetings?from={iso_format_time}"

    # Выполняем GET-запрос
    response = requests.get(url, headers=sessionManager.get_headers(), timeout=10)
    if response.status_code == 200:
        response_data = response.json()
        meetings = response_data.get("meetings", [])
        return meetings
    return []


def add_meeting(meeting_data):
    """Отправляет запрос на создание встречи."""
    url = f"{HOST_URL}/api/v1/meetings/add"
    response = requests.post(
        url, json=meeting_data, headers=sessionManager.get_headers(), timeout=10
    )

    if response.status_code == 200:
        return True
    else:
        raise Exception(f"Ошибка при добавлении встречи: {response.status_code}, {response.text}")
