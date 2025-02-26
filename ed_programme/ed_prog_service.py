"""
ed_prog_service - Модуль для работы с учебными направлениями

Этот модуль работает с API
"""
import requests
from bot.bot import HOST_URL, sessionManager


def get_educational_programmes():
    """функция для получения учебных программ"""
    response = requests.get(
        f"{HOST_URL}/api/v1/universities/1/edprogrammes/",
        headers=sessionManager.get_headers(),
        timeout=10,
    )
    if response.status_code == 200:
        response_data = response.json()
        educational_programmes = response_data.get("programmes", [])
        return educational_programmes  # Возвращает список образовательных программ в формате JSON
    return []
