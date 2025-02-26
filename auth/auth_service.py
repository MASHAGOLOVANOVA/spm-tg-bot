"""
auth_service - Модуль для обработки аутентификации пользователей.

Этот модуль работает с API
"""
import requests
from bot.bot import HOST_URL, sessionManager


def send_verification_request(credentials):
    """Отправляет запрос на проверку номера и возвращает ответ."""
    response = requests.post(
        HOST_URL + "/api/v1/auth/bot/signinuser",
        json=credentials,
        headers=sessionManager.get_headers(),
        timeout=10,
    )
    return response


def get_account():
    """функция для получения аккаунта"""
    response = requests.get(
        f"{HOST_URL}/api/v1/account", headers=sessionManager.get_headers(), timeout=10
    )
    if response.status_code == 200:
        account = response.json()
        return account
    return []
