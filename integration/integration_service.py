"""
integration_service - Модуль для работы с интеграциями пользователя

Этот модуль работает с API
"""
import requests
from bot.bot import HOST_URL, sessionManager


def get_integrations():
    """функция для получения интеграций"""
    integrations_response = requests.get(
        f"{HOST_URL}/api/v1/account/integrations",
        headers=sessionManager.get_headers(),
        timeout=10,
    )
    return integrations_response
