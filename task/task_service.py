"""
task_service - Модуль для работы с задачами

Этот модуль работает с API
"""
import requests
from bot.bot import HOST_URL, sessionManager


def add_task_to_project(project_id, task_data):
    """Выполняет запрос для добавления задачи в проект."""
    url = f"{HOST_URL}/api/v1/projects/{project_id}/tasks/add"
    response = requests.post(url, json=task_data, headers=sessionManager.get_headers(), timeout=10)
    return response


def get_project_tasks(project_id):
    """Выполняет запрос для получения задач проекта."""
    url = f"{HOST_URL}/api/v1/projects/{project_id}/tasks"
    response = requests.get(url, headers=sessionManager.get_headers(), timeout=10)

    if response.status_code == 200:
        return response.json().get("tasks", [])
    raise Exception(f"Ошибка при получении задач: {response.status_code}")
