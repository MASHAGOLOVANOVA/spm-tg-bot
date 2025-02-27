# -*- coding: utf-8 -*-
"""Этот модуль реализует функциональность бота Telegram."""
import os
import telebot
from dotenv import load_dotenv

from session_manager import SessionManager

load_dotenv()

HOST_URL = os.getenv("HOST_URL", "http://localhost:8080")
CLIENT_URL = os.getenv("CLIENT_URL", "http://localhost:3000")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7772483926:AAFkT_nibrVHwZmlJajxbXRU4Wxe_b7t_RI")
bot = telebot.TeleBot(BOT_TOKEN)
sessionManager = SessionManager()
sessionManager.set_bot_token(BOT_TOKEN)


def update_session_token(new_token):
    """# Функция для обновления session_token"""
    sessionManager.set_session_token(new_token)
