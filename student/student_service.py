"""
student_service - Модуль для работы со студентами

Этот модуль работает с API
"""
import requests
from bot.bot import HOST_URL, sessionManager


def get_students():
    """функция для получения студентов"""
    response = requests.get(
        f"{HOST_URL}/api/v1/students", headers=sessionManager.get_headers(), timeout=10
    )
    if response.status_code == 200:
        response_data = response.json()
        students = response_data.get("students", [])
        return students  # Возвращает список студентов в формате JSON
    return []


def add_student(student_data):
    """Добавляет нового студента через API."""
    response = requests.post(
        f"{HOST_URL}/api/v1/students/add",
        json=student_data,
        headers=sessionManager.get_headers(),
        timeout=10,
    )
    return response
