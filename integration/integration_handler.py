"""
integration_handler - Модуль для работы с интеграциями пользователя
"""
from integration.integration_service import get_integrations


def get_cloud_drive():
    """функция для получения интеграции с диском"""
    integrations = get_integrations()
    try:
        response_json = integrations.json()
        if "cloud_drive" in response_json:
            return response_json["cloud_drive"]
        print("Cloud Drive не найден.")
        return None
    except ValueError as e:
        print(f"Ошибка при обработке JSON: {e}")
        return None


def get_google_planner():
    """функция для получения интеграции с планнером"""
    integrations = get_integrations()
    try:
        response_json = integrations.json()
        # Проверяем наличие "cloud_drive"
        if "planner" in response_json:
            if "planner_name" in response_json["planner"]:
                return response_json["planner"]["planner_name"]
            return None
        print("Cloud Calendar не найден.")
        return None
    except ValueError as e:
        print(f"Ошибка при обработке JSON: {e}")
        return None


def get_repohub():
    """функция для получения интеграции с гитхабом"""
    integrations = get_integrations()
    if integrations.status_code == 200:
        integrations_data = integrations.json()  # Преобразуем в JSON
        if len(integrations_data["repo_hubs"]) > 0:
            return integrations_data["repo_hubs"]
    print(f"Ошибка при получении интеграций: {integrations.status_code}")
    return None
