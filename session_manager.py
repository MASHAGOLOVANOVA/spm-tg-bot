"""
session_manager - Класс для headers запросов по API
"""
class SessionManager:
    """Класс для получении инфы о сессии"""

    def __init__(self):
        """Класс для получении инфы о сессии"""
        self.session_token = None
        self.bot_token = None

    def set_session_token(self, token):
        """функция для апдейта токена"""
        self.session_token = token

    def set_bot_token(self, token):
        self.bot_token = token

    def get_headers(self):
        """функция для получения хедеров запросов"""
        return {
            "Content-Type": "application/json",
            "Bot-Token": self.bot_token,
            "tuna-skip-browser-warning": "please",
            "Session-Id": self.session_token,
        }
