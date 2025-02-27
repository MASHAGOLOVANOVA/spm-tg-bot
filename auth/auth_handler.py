"""
auth_handler - Модуль для обработки аутентификации пользователей.

Этот модуль содержит функции и классы, необходимые для управления
аутентификацией пользователей в приложении.
"""
from requests.exceptions import RequestException
from bot.bot import CLIENT_URL, update_session_token
from auth.auth_service import send_verification_request, get_account
from menu.menu_handler import show_main_menu
from integration.integration_handler import get_cloud_drive


def auth_handler_init(bot):
    """Хендлер init"""
    @bot.message_handler(content_types=["contact"])
    def handle_contact(message):
        """Хендлер contact"""
        contact = message.contact
        phone_number = contact.phone_number  # Получаем номер телефона
        bot.send_message(message.chat.id, f"Спасибо! Ваш номер телефона: {phone_number}")

        # Создаем данные для отправки на сервер
        credentials = {"phone_number": phone_number}
        verify_number(message, credentials)

    def verify_number(message, credentials):
        """Функция для поиска номера в системе"""
        try:
            bot.send_message(message.chat.id, "Проверяем регистрацию...")

            response = send_verification_request(credentials)  # Отправляем запрос

            handle_verification_response(message, response)  # Обрабатываем ответ

        except RequestException as e:
            bot.send_message(message.chat.id, f"Ошибка сети: {str(e)}")

    def handle_verification_response(message, response):
        """Обрабатывает ответ от API и выполняет соответствующие действия."""
        if response.status_code == 200:
            bot.send_message(message.chat.id, "Мы Вас нашли!")

            response_data = response.json()  # Используем response.json()

            # Обновляем session_token, если он присутствует в ответе
            if "session_token" in response_data:
                update_session_token(response_data["session_token"])
                professor = get_account()
                bot.send_message(message.chat.id, f'Здравствуйте, {professor["name"]}!')
                cloud_drive = get_cloud_drive()
                if cloud_drive is not None:
                    show_main_menu(message.chat.id)
                else:
                    bot.send_message(
                        message.chat.id,
                        f"""Чтобы воспользоваться функциями бота подключите
Google Drive из веб-приложения:\n{CLIENT_URL}/profile/integrations""",
                    )
            else:
                print("session_token не найден в ответе")
        else:
            bot.send_message(
                message.chat.id,
                "Произошла ошибка при поиске пользователя по номеру телефона.",
            )
